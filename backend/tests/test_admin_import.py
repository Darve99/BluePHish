def test_admin_service_is_available_for_main_app():
    from app.admin import admin_service

    assert admin_service is not None
    assert hasattr(admin_service, "list_rules")
    assert hasattr(admin_service, "stats")
