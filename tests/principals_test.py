from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 64,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 3,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B



"""following are the 6 extra test cases """

def test_grade_assignment_not_found(client, h_principal):
        """
        Test case for grading a non-existent assignment.
        """
          
        response = client.post(
            '/principal/assignments/grade',
            json={
                'id': 9999,  # Assuming this ID does not exist
                'grade': GradeEnum.A.value
            },
            headers=h_principal
        )

        assert response.status_code == 404  # Expecting a not found error


def test_grade_assignment_invalid_grade(client, h_principal):
    """
    Test case for grading an assignment with an invalid grade.
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': 'INVALID_GRADE'  # Invalid grade input
        },
        headers=h_principal
    )

    assert response.status_code == 400  # Expecting a bad request error



def test_view_all_teachers(client, h_principal):
    """
    Test case for a principal viewing all teachers.
    """
    # Send a GET request to the endpoint to retrieve the list of teachers
    response = client.get('/principal/teachers', headers=h_principal)

    # Check that the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Verify that the response is in the expected format
    assert isinstance(response.json, dict)  # Ensure response is a dictionary
    assert 'data' in response.json  # Check if 'data' key exists

    # Check that the 'data' key contains a list of teachers
    teachers_data = response.json['data']
    assert isinstance(teachers_data, list)  # Expecting a list of teachers

    # Optionally, you can check if there are any teachers returned
    assert len(teachers_data) > 0  # Ensure that at least one teacher is present

    # Optional: Check if each teacher object has expected properties
    for teacher in teachers_data:
        assert 'id' in teacher  # Check for 'id' key
        assert 'user_id' in teacher  # Check for 'user_id' key
        assert 'created_at' in teacher  # Check for 'created_at' key
        assert 'updated_at' in teacher  # Check for 'updated_at' key
