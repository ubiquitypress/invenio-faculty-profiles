from copy import deepcopy
from io import BytesIO


def test_resource(
    app,
    db,
    users,
    headers,
    search_clear,
    search,
    employee_profile_data,
    location,
    admin_client,
):
    # Create
    with admin_client.post(
        "/faculty-profiles", headers=headers, json=employee_profile_data
    ) as response:
        assert response.status_code == 201
        data = response.json
        assert data["metadata"] == {
            "preferred_pronouns": "Mr",
            "family_name": "Doe",
            "given_names": "John",
            "identifiers": [{"identifier": "0000-0002-1825-0097", "scheme": "orcid"}],
            "biography": "John Doe is a software engineer with over 10 years of experience in the tech industry. He specializes in backend development, particularly with Python and Django. He has a passion for clean, efficient code and enjoys working on complex, challenging problems.",
            "interests": "death",
            "title_status": "Professor",
            "department": "Biology",
            "institution": "Jail",
            "education": "some",
            "email_address": "johndoe@example.com",
            "contact_email_address": "johndoe-contact@example.com",
        }
        id_ = data["id"]

    with admin_client.get(f"/faculty-profiles/{id_}") as response:
        assert response.status_code == 200

    # Update Record
    employee_profile_data["metadata"]["email_address"] = "jakecollins1976@gmail.com"
    with admin_client.put(
        f"/faculty-profiles/{id_}", json=employee_profile_data
    ) as response:
        assert response.json["metadata"]["email_address"] == "jakecollins1976@gmail.com"
        assert response.status_code == 200

    # Delete Record
    with admin_client.delete(f"/faculty-profiles/{id_}") as response:
        assert response.status_code == 204

    # No Longer exists
    with admin_client.get(f"/faculty-profiles/{id_}") as response:
        assert response.status_code == 404


def test_photo_flow(
    app,
    db,
    users,
    search_clear,
    search,
    employee_profile_data,
    location,
    admin_client,
    headers,
):
    """Test photo workflow."""
    # Create an employee Profile
    res = admin_client.post("/faculty-profiles", json=employee_profile_data)
    assert res.status_code == 201
    created_ep = res.json
    id_ = created_ep["id"]

    assert (
        created_ep["links"]["photo"]
        == f"https://127.0.0.1:5000/api/faculty-profiles/{id_}/photo"
    )

    # Get non-existent photo
    res = admin_client.get(f"/faculty-profiles/{id_}/photo")
    assert res.status_code == 404
    assert res.json["message"] == "No file exists for this faculty profile."

    # Delete non-existent photo
    res = admin_client.delete(f"/faculty-profiles/{id_}/photo", headers=headers)
    assert res.status_code == 404
    assert res.json["message"] == "No file exists for this faculty profile."

    # Update photo
    res = admin_client.put(
        f"/faculty-profiles/{id_}/photo",
        headers={
            **headers,
            "content-type": "application/octet-stream",
            "X-Filename": "photo.jpg",
        },
        data=BytesIO(b"photo"),
    )
    assert res.status_code == 200
    assert res.json["size"] == 5

    # Get photo
    res = admin_client.get(f"/faculty-profiles/{id_}/photo")
    assert res.status_code == 200
    assert res.data == b"photo"

    # Update photo again
    res = admin_client.put(
        f"/faculty-profiles/{id_}/photo",
        headers={
            **headers,
            "content-type": "application/octet-stream",
            "X-Filename": "photo.gif",
        },
        data=BytesIO(b"new_photo"),
    )
    assert res.status_code == 200
    assert res.json["size"] == 9

    # Get new photo
    res = admin_client.get(f"/faculty-profiles/{id_}/photo")
    assert res.status_code == 200
    assert res.data == b"new_photo"

    res = admin_client.get(f"/faculty-profiles/{id_}")
    # Delete photo with unauthorized user
    with app.test_client() as anon_client:
        res = anon_client.delete(f"/faculty-profiles/{id_}/photo", headers=headers)
        assert res.status_code == 403

    # Delete photo
    res = admin_client.delete(f"/faculty-profiles/{id_}/photo", headers=headers)
    assert res.status_code == 204

    # Try to get deleted photo
    res = admin_client.get(f"/faculty-profiles/{id_}/photo")
    assert res.status_code == 404
    assert res.json["message"] == "No file exists for this faculty profile."


def test_cv_flow(
    app,
    db,
    users,
    search_clear,
    search,
    employee_profile_data,
    location,
    admin_client,
    headers,
):
    """Test cv workflow."""
    # Create an employee Profile
    res = admin_client.post("/faculty-profiles", json=employee_profile_data)
    assert res.status_code == 201
    created_ep = res.json
    id_ = created_ep["id"]

    assert (
        created_ep["links"]["cv"]
        == f"https://127.0.0.1:5000/api/faculty-profiles/{id_}/cv"
    )

    # Get non-existent cv
    res = admin_client.get(f"/faculty-profiles/{id_}/cv")
    assert res.status_code == 404
    assert res.json["message"] == "No file exists for this faculty profile."

    # Delete non-existent cv
    res = admin_client.delete(f"/faculty-profiles/{id_}/cv", headers=headers)
    assert res.status_code == 404
    assert res.json["message"] == "No file exists for this faculty profile."

    # Update cv
    res = admin_client.put(
        f"/faculty-profiles/{id_}/cv",
        headers={
            **headers,
            "content-type": "application/octet-stream",
            "X-Filename": "cv-2345.docx",
        },
        data=BytesIO(b"cv"),
    )
    assert res.status_code == 200
    assert res.json["size"] == 2

    # Get cv
    res = admin_client.get(f"/faculty-profiles/{id_}/cv")
    assert res.status_code == 200
    assert res.data == b"cv"

    # Update cv again
    res = admin_client.put(
        f"/faculty-profiles/{id_}/cv",
        headers={
            **headers,
            "content-type": "application/octet-stream",
            "X-Filename": "cv-3345.pdf",
        },
        data=BytesIO(b"new_cv"),
    )
    assert res.status_code == 200
    assert res.json["size"] == 6

    # Get new cv
    res = admin_client.get(f"/faculty-profiles/{id_}/cv")
    assert res.status_code == 200
    assert res.data == b"new_cv"

    res = admin_client.get(f"/faculty-profiles/{id_}")

    # Delete cv with unauthorized user
    with app.test_client() as anon_client:
        res = anon_client.delete(f"/faculty-profiles/{id_}/cv", headers=headers)
        assert res.status_code == 403

    # Delete cv
    res = admin_client.delete(f"/faculty-profiles/{id_}/cv", headers=headers)
    assert res.status_code == 204

    # Try to get deleted cv
    res = admin_client.get(f"/faculty-profiles/{id_}/cv")
    assert res.status_code == 404
    assert res.json["message"] == "No file exists for this faculty profile."


def test_photo_max_content_length(
    app,
    db,
    users,
    search_clear,
    search,
    employee_profile_data,
    location,
    admin_client,
    headers,
):
    """Test photo max size."""

    # Create an employee Profile
    res = admin_client.post("/faculty-profiles", json=employee_profile_data)
    assert res.status_code == 201
    created_ep = res.json
    id_ = created_ep["id"]
    assert (
        created_ep["links"]["photo"]
        == f"https://127.0.0.1:5000/api/faculty-profiles/{id_}/photo"
    )

    # Update app max size for community photos
    max_size = 10**6
    app.config["FACULTY_PROFILES_PHOTO_MAX_FILE_SIZE"] = max_size

    # Update photo with big content
    photo_data = b"photo" * (max_size + 1)
    res = admin_client.put(
        f"/faculty-profiles/{id_}/photo",
        headers={
            **headers,
            "content-type": "application/octet-stream",
        },
        data=BytesIO(photo_data),
    )
    assert res.status_code == 400

    # Update photo with small content
    photo_data = b"photo"
    res = admin_client.put(
        f"/faculty-profiles/{id_}/photo",
        headers={
            **headers,
            "content-type": "application/octet-stream",
        },
        data=BytesIO(photo_data),
    )
    assert res.status_code == 200


def test_faculty_profiles_search_config(client):
    """Test community search config."""
    res = client.get("/config/faculty-profiles-search-config")
    assert res.status_code == 200

    data = res.json

    assert list(data.keys()) == [
        "appId",
        "initialQueryState",
        "searchApi",
        "sortOptions",
        "aggs",
        "layoutOptions",
        "sortOrderDisabled",
        "paginationOptions",
        "defaultSortingOnEmptyQueryString",
    ]
    assert data["appId"] == "search"
