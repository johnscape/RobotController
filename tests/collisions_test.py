from objectData.objectView import LineCollision, Verticle2D, Verticle, Face, LineFaceCollision, VerticleDistance


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

def test_faceCollision3D():
    v1 = Verticle(4, 0, 0)
    v2 = Verticle(3, 4, 3)
    v3 = Verticle(2, 2, 2)

    p1 = Verticle(1, 1, -1)
    p2 = Verticle(5, 2, 3)

    f = Face(v1, v2, v3)

    assert f.CollisionCheck(p1, p2) is True

def test_falseFaceCollision3D():
    v1 = Verticle(4, 0, 0)
    v2 = Verticle(3, 4, 3)
    v3 = Verticle(2, 2, 2)

    p1 = Verticle(0, 0, 0)
    p2 = Verticle(2, 1, 0)

    f = Face(v1, v2, v3)

    assert f.CollisionCheck(p1, p2) is False

def test_collisionDistance():
    v1 = Verticle(0.2, 0.6, 0)
    v2 = Verticle(0.6, 0.6, 0)
    v3 = Verticle(0.4, 0.7, 0.4)

    p1 = Verticle(0.4, 0, 0.2)
    p2 = Verticle(0.4, 1, 0.2)

    f = Face(v1, v2, v3)

    errors = []

    collSuccess = f.CollisionCheck(p1, p2) is True
    if not collSuccess:
        errors.append("Collision value is false!")
    else:
        colPoint = LineFaceCollision(f, p1, p2)
        distSuccess = VerticleDistance(colPoint, Verticle(0.4, 0.65, 0.2)) < 0.1 # error treshold
        if not distSuccess:
            errors.append("Collision did not happened at the predicted point. Collision was at: {0} | {1} | {2}".format(colPoint.X, colPoint.Y, colPoint.Z))

    assert not errors, "errors occured:\n{}".format("\n".join(errors))