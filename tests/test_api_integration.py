import requests


# Test species API
def test_race_api():
    response = requests.get("https://www.dnd5eapi.co/api/races")
    assert response.status_code == 200
    assert "Dragonborn" in response.json()["results"][0]["name"]
    assert "Dwarf" in response.json()["results"][1]["name"]


# Test class API
def test_class_api():
    response = requests.get("https://www.dnd5eapi.co/api/classes")
    assert response.status_code == 200
    assert "Barbarian" in response.json()["results"][0]["name"]
    assert "Bard" in response.json()["results"][1]["name"]
