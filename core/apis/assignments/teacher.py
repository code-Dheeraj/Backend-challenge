from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.libs import assertions
from core.libs.exceptions import FyleError
from core.models.assignments import Assignment, AssignmentStateEnum

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)




@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments for the authenticated teacher."""
    teacher_id = p.teacher_id  # Extract the teacher_id from the authenticated principal object
    # Fetch only assignments with the state 'SUBMITTED' or 'GRADED'
    teachers_assignments = Assignment.query.filter_by(teacher_id=teacher_id).filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    # Load and validate the payload using the schema
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Fetch the assignment by id
    assignment = Assignment.get_by_id(grade_assignment_payload.id)

    # Ensure the assignment exists
    assertions.assert_found(assignment, 'No assignment with this id was found')

    # Check if the assignment was submitted to the authenticated teacher
    if assignment.teacher_id != p.teacher_id:
        # Pass the required 'status_code' and 'message'
        raise FyleError(status_code=400, message='Assignment was not submitted to this teacher')

    # Ensure the assignment is not in the DRAFT state
    if assignment.state == AssignmentStateEnum.DRAFT:
        raise FyleError(status_code=400, message='Assignment is in draft state and cannot be graded')

    # Proceed with grading the assignment
    graded_assignment = Assignment.mark_grade(
        grade_assignment_payload.id,
        grade_assignment_payload.grade,
        p
    )

    db.session.commit()

    # Dump the graded assignment for the response
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)

