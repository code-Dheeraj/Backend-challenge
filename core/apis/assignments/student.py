from flask import Blueprint, abort
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment,AssignmentStateEnum

from .schema import AssignmentSchema, AssignmentSubmitSchema
student_assignments_resources = Blueprint('student_assignments_resources', __name__)


@student_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    students_assignments = Assignment.get_assignments_by_student(p.student_id)
    students_assignments_dump = AssignmentSchema().dump(students_assignments, many=True)
    return APIResponse.respond(data=students_assignments_dump)


# @student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def upsert_assignment(p, incoming_payload):
#     """Create or Edit an assignment"""
#     assignment = AssignmentSchema().load(incoming_payload)
#     assignment.student_id = p.student_id

#     upserted_assignment = Assignment.upsert(assignment)
#     db.session.commit()
#     upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)
#     return APIResponse.respond(data=upserted_assignment_dump)

#----------------------------------------------------
@student_assignments_resources.route('/assignments', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def upsert_assignment(p, incoming_payload):
    """Create or Edit an assignment"""
    # Load the incoming payload into a dictionary
    assignment_data = AssignmentSchema().load(incoming_payload)

    # Create a new Assignment instance or retrieve the existing one
    assignment = Assignment(**assignment_data)

    # Assign the student_id from the authenticated principal
    assignment.student_id = p.student_id

    # Upsert the assignment into the database (insert or update)
    upserted_assignment = Assignment.upsert(assignment)

    # Commit the changes to the database
    db.session.commit()

    # Serialize the upserted assignment for response
    upserted_assignment_dump = AssignmentSchema().dump(upserted_assignment)

    # Return the response
    return APIResponse.respond(data=upserted_assignment_dump)








#-----------------------------------------------------


# @student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def submit_assignment(p, incoming_payload):
#     """Submit an assignment"""
#     submit_assignment_payload = AssignmentSubmitSchema().load(incoming_payload)

#     submitted_assignment = Assignment.submit(
#         _id=submit_assignment_payload.id,
#         teacher_id=submit_assignment_payload.teacher_id,
#         auth_principal=p
#     )
#     db.session.commit()
#     submitted_assignment_dump = AssignmentSchema().dump(submitted_assignment)
#     return APIResponse.respond(data=submitted_assignment_dump)





# @student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def submit_assignment(p, incoming_payload):
#     """Submit an assignment"""
#     # Load the incoming payload
#     submit_payload = AssignmentSubmitSchema().load(incoming_payload)

#     # Fetch the assignment by ID
#     assignment = Assignment.get_by_id(submit_payload.id)

#     # Check if the assignment belongs to the student
#     if assignment.student_id != p.student_id:
#         abort(403, description="You do not have permission to submit this assignment.")

#     # Update the state to SUBMITTED
#     assignment.state = AssignmentStateEnum.SUBMITTED
#     assignment.teacher_id = submit_payload.teacher_id  # Set the teacher ID

#     # Commit the transaction to the database
#     db.session.commit()

#     # Serialize the updated assignment data
#     updated_assignment_dump = AssignmentSchema().dump(assignment)

#     return APIResponse.respond(data=updated_assignment_dump)


@student_assignments_resources.route('/assignments/submit', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def submit_assignment(p, incoming_payload):
    """Submit an assignment"""
    # Load the incoming payload
    submit_payload = AssignmentSubmitSchema().load(incoming_payload)

    # Fetch the assignment by ID
    assignment = Assignment.get_by_id(submit_payload.id)

    # Check if the assignment belongs to the student
    if assignment.student_id != p.student_id:
        abort(403, description="You do not have permission to submit this assignment.")

    # Check if the assignment is already submitted
    if assignment.state == AssignmentStateEnum.SUBMITTED:
        return {
            'error': 'FyleError',
            'message': 'only a draft assignment can be submitted'
        }, 400

    # Update the state to SUBMITTED
    assignment.state = AssignmentStateEnum.SUBMITTED
    assignment.teacher_id = submit_payload.teacher_id  # Set the teacher ID

    # Commit the transaction to the database
    db.session.commit()

    # Serialize the updated assignment data
    updated_assignment_dump = AssignmentSchema().dump(assignment)

    return APIResponse.respond(data=updated_assignment_dump)



