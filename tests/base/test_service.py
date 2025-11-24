from deployer.service import Service


def test_create_service():
    service = Service("test")

    assert service.name == "test"
