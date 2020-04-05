from objectData.ObjLoader import LineCollision, Verticle2D, Verticle, Face


def test_LineCollision():
    p1 = Verticle2D(0, 0)
    p2 = Verticle2D(5, 5)

    p3 = Verticle2D(0, 4)
    p4 = Verticle2D(6, 4)

    assert LineCollision(p1, p2, p3, p4) is True

def test_falseLineCollision():
    p1 = Verticle2D(0, 0)
    p2 = Verticle2D(5, 5)

    p3 = Verticle2D(0, 4)
    p4 = Verticle2D(3, 4)

    assert LineCollision(p1, p2, p3, p4) is False

def test_faceCollision2D():
    v1 = Verticle(3, 0, 0)
    v2 = Verticle(5, 0, 3)
    v3 = Verticle(7, 0, 0)

    p1 = Verticle(2, 0, 2)
    p2 = Verticle(8, 0, 2)

    f = Face(v1, v2, v3)
    
    assert f.CollisionCheck(p1, p2) is True

def test_falseFaceCollision2D():
    v1 = Verticle(3, -1, 0)
    v2 = Verticle(5, -1, 3)
    v3 = Verticle(7, -1, 0)

    p1 = Verticle(2, 0, 2)
    p2 = Verticle(8, 30, 2)

    f = Face(v1, v2, v3)

    assert f.CollisionCheck(p1, p2) is False