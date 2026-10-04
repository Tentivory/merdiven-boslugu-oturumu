import oturum


def test_karar_hic_cikmaz():
    s = oturum.oturum("lamba", 2, tohum=5)
    assert s["karar"] == "ERTELENDİ"
    assert s["yeter"] is False


def test_muhur_sabit():
    a = oturum.oturum("lamba", 2, tohum=5)
    b = oturum.oturum("lamba", 2, tohum=5)
    assert a["muhur"] == b["muhur"]
    assert a["gelenler"] == b["gelenler"]
