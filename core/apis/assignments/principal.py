from flask import Blueprint,abort
from core.models.teachers import Teacher
from core.models.assignments import Assignment,AssignmentStateEnum
from core.apis.assignments.schema import AssignmentSchema, TeacherSchema, AssignmentGradeSchema
from core.apis import decorators
from core.apis.responses import APIResponse
from core import db
from marshmallow import Schema, fields, post_load


# Create a Blueprint for the principal API
principal_api = Blueprint('principal_api', __name__)

# @principal_api.route('/principal/teachers', methods=['GET'], strict_slashes=False)
# @decorators.authenticate_principal
# def list_teachers(principal):
#     """Returns a list of teachers"""
#     # Retrieve all teachers from the database
#     teachers = Teacher.query.all()
    
#     # Serialize the data using TeacherSchema
#     teachers_schema = TeacherSchema(many=True)
#     teachers_dump = teachers_schema.dump(teachers)

#     # Format response
#     response_data = {"data": teachers_dump}
#     return APIResponse.respond(response_data)

# @principal_api.route('/principal/teachers', methods=['GET'], strict_slashes=False)
# @decorators.authenticate_principal
# def list_teachers(principal):
#     """Returns a list of teachers."""
#     # Retrieve all teachers from the database
#     teachers = Teacher.query.all()
    
#     # Serialize the data using TeacherSchema
#     teachers_schema = TeacherSchema(many=True)
#     teachers_dump = teachers_schema.dump(teachers)

#     # Format response
#     response_data = {"data": teachers_dump}
#     return APIResponse.respond(response_data)

@principal_api.route('/principal/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(principal):
    """Returns a list of teachers."""
    # Retrieve all teachers from the database
    teachers = Teacher.query.all()
    
    # Serialize the data using TeacherSchema
    teachers_schema = TeacherSchema(many=True)
    teachers_dump = teachers_schema.dump(teachers)

    # Format response
    return APIResponse.respond(teachers_dump)  # Send the list directly




#--------------------------------------------------------------------------------------------------------------------



@principal_api.route('/principal/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(principal):
    """Returns a list of submitted and graded assignments"""
    # Retrieve all assignments that are submitted and graded
    assignments = Assignment.filter( Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()

    
    # Serialize the data using AssignmentSchema
    assignment_schema = AssignmentSchema(many=True)
    assignments_dump = assignment_schema.dump(assignments)

    # Format response
    response_data =  assignments_dump
    return APIResponse.respond(response_data)


#--------------------------------------------------------------------------------------------------------------------
# @principal_api.route('/principal/assignments/grade', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def grade_assignment(principal, incoming_payload):
#     """Grade or re-grade an assignment"""
#     # Validate and load the incoming payload using the schema
#     grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

#     # Grade the assignment
#     graded_assignment = Assignment.mark_grade(
#         _id=grade_assignment_payload.id,
#         grade=grade_assignment_payload.grade,
#         auth_principal=principal
#     )
    
#     # Commit the transaction to the database
#     db.session.commit()

#     # Serialize the graded assignment data
#     graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

#     # Format response to match the required structure
#     response_data = {"data": graded_assignment_dump}
#     return APIResponse.respond(response_data)

# @principal_api.route('/principal/assignments/grade', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def grade_assignment(principal, incoming_payload):
#     """Grade or re-grade an assignment"""
#     # Validate and load the incoming payload using the schema
#     grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

#     # Fetch the assignment by ID
#     assignment = Assignment.get_by_id(grade_assignment_payload.id)

#     # Check if the assignment is in a valid state for grading
#     if assignment.state == AssignmentStateEnum.DRAFT:
#         # Raise 400 if the assignment is in the DRAFT state
#         abort(400, description="Cannot grade a draft assignment.")
    
#     if assignment.state not in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]:
#         # Raise 400 if the assignment is not in SUBMITTED or GRADED state
#         abort(400, description="Assignment must be submitted or already graded.")

#     # Grade the assignment
#     graded_assignment = Assignment.mark_grade(
#         _id=grade_assignment_payload.id,
#         grade=grade_assignment_payload.grade,
#         auth_principal=principal
#     )
    
#     # Commit the transaction to the database
#     db.session.commit()

#     # Serialize the graded assignment data
#     graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

#     # Format response to match the required structure
#     response_data = {"data": graded_assignment_dump}
#     return APIResponse.respond(response_data)



# @principal_api.route('/principal/assignments/grade', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def grade_assignment(principal, incoming_payload):
#     """Grade or re-grade an assignment"""
#     # Validate and load the incoming payload using the schema
#     grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

#     # Fetch the assignment by ID
#     assignment = Assignment.get_by_id(grade_assignment_payload.id)

#     # Check if the assignment is in a valid state for grading
#     if assignment.state == AssignmentStateEnum.DRAFT:
#         # Raise 400 if the assignment is in the DRAFT state
#         abort(400, description="Cannot grade a draft assignment.")
    
#     if assignment.state not in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]:
#         # Raise 400 if the assignment is not in SUBMITTED or GRADED state
#         abort(400, description="Assignment must be submitted or already graded.")

#     # Update the state to GRADED if the assignment is being graded
#     assignment.state = AssignmentStateEnum.GRADED

#     # Grade the assignment
#     graded_assignment = Assignment.mark_grade(
#         _id=grade_assignment_payload.id,
#         grade=grade_assignment_payload.grade,
#         auth_principal=principal
#     )
    
#     # Commit the transaction to the database
#     db.session.commit()

#     # Serialize the graded assignment data, including the state
#     graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

#     # Ensure the state is included in the serialized response
#     graded_assignment_dump['state'] = assignment.state

#     # Format response to match the required structure
#     response_data = {"data": graded_assignment_dump}
#     return APIResponse.respond(response_data)


# @principal_api.route('/principal/assignments/grade', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def grade_assignment(principal, incoming_payload):
#     """Grade or re-grade an assignment"""
#     # Validate and load the incoming payload using the schema
#     grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

#     # Fetch the assignment by ID
#     assignment = Assignment.get_by_id(grade_assignment_payload.id)

#     # Check if the assignment is in a valid state for grading
#     if assignment.state == AssignmentStateEnum.DRAFT:
#         # Raise 400 if the assignment is in the DRAFT state
#         abort(400, description="Cannot grade a draft assignment.")
    
#     if assignment.state not in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]:
#         # Raise 400 if the assignment is not in SUBMITTED or GRADED state
#         abort(400, description="Assignment must be submitted or already graded.")

#     # Update the state to GRADED if the assignment is being graded
#     assignment.state = AssignmentStateEnum.GRADED

#     # Grade the assignment
#     graded_assignment = Assignment.mark_grade(
#         _id=grade_assignment_payload.id,
#         grade=grade_assignment_payload.grade,
#         auth_principal=principal
#     )
    
#     # Commit the transaction to the database
#     db.session.commit()

#     # Serialize the graded assignment data, including the state
#     graded_assignment_dump = AssignmentSchema().dump(graded_assignment)

#     # Format the response to return the assignment in a list format
#     response_data = {
#         "data": [graded_assignment_dump]  # Wrap the result in a list
#     }
    
#     return APIResponse.respond(response_data)

# @principal_api.route('/principal/assignments/grade', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def grade_assignment(principal, incoming_payload):
#     """Grade or re-grade an assignment"""
#     # Validate and load the incoming payload using the schema
#     grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

#     # Fetch the assignment by ID
#     assignment = Assignment.get_by_id(grade_assignment_payload.id)

#     # Check if the assignment is in a valid state for grading
#     if assignment.state == AssignmentStateEnum.DRAFT:
#         abort(400, description="Cannot grade a draft assignment.")
    
#     if assignment.state not in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]:
#         abort(400, description="Assignment must be submitted or already graded.")

#     # Update the state to GRADED if the assignment is being graded
#     assignment.state = AssignmentStateEnum.GRADED

#     # Grade the assignment
#     graded_assignment = Assignment.mark_grade(
#         _id=grade_assignment_payload.id,
#         grade=grade_assignment_payload.grade,
#         auth_principal=principal
#     )
    
#     # Commit the transaction to the database
#     db.session.commit()

#     # Ensure all required fields are serialized correctly
#     graded_assignment_dump = {
#         "id": graded_assignment.id,
#         "content": graded_assignment.content,
#         "created_at": graded_assignment.created_at.isoformat(),
#         "updated_at": graded_assignment.updated_at.isoformat(),
#         "grade": graded_assignment.grade.value if graded_assignment.grade else None,
#         "state": graded_assignment.state,
#         "student_id": graded_assignment.student_id,
#         "teacher_id": graded_assignment.teacher_id
#     }

#     # Format response to include a list of the graded assignment
#     response_data = graded_assignment_dump  # Ensure it's a list
    
#     return APIResponse.respond(response_data)


#--------------------------------------------------------------------------------------------------------------------


@principal_api.route('/principal/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(principal, incoming_payload):
    """Grade or re-grade an assignment"""
    # Validate and load the incoming payload using the schema
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    # Fetch the assignment by ID
    assignment = Assignment.get_by_id(grade_assignment_payload.id)

    # Check if the assignment exists
    if assignment is None:
        abort(404, description="Assignment not found.")

    # Check if the assignment is in a valid state for grading
    if assignment.state == AssignmentStateEnum.DRAFT:
        abort(400, description="Cannot grade a draft assignment.")

    if assignment.state not in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]:
        abort(400, description="Assignment must be submitted or already graded.")

    # Update the state to GRADED if the assignment is being graded
    assignment.state = AssignmentStateEnum.GRADED

    # Grade the assignment
    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=principal
    )
    
    # Commit the transaction to the database
    db.session.commit()

    # Ensure all required fields are serialized correctly
    graded_assignment_dump = {
        "id": graded_assignment.id,
        "content": graded_assignment.content,
        "created_at": graded_assignment.created_at.isoformat(),
        "updated_at": graded_assignment.updated_at.isoformat(),
        "grade": graded_assignment.grade.value if graded_assignment.grade else None,
        "state": graded_assignment.state,
        "student_id": graded_assignment.student_id,
        "teacher_id": graded_assignment.teacher_id
    }

    # Format response to include a list of the graded assignment
    response_data = graded_assignment_dump  # Ensure it's a list
    
    return APIResponse.respond(response_data)
#--------------------------------------------------------------------------------------------------------------------
