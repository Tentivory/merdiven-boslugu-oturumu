#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merdiven boşluğu oturumu.

Katlar söz alır, yeter sayı tutmaz, gündem ertelenir.
Çalışır. Karar çıkmaz. Bu spesifikasyondur.
"""

from __future__ import annotations

import argparse
import hashlib
import random
import sys
from datetime import datetime

KATLAR = [
    "zemin (kapıyı tutuyor)",
    "1. kat (terlik sesi)",
    "2. kat (yemek kokusu sözcüsü)",
    "3. kat (perde aralığı gözlemcisi)",
    "4. kat (asansörle kavgalı)",
    "5. kat (hiç evde değil, yine de oy kullanır)",
    "6. kat (fısıltı komisyonu)",
    "çatı arası (depo, söz hakkı yok, yine konuşur)",
]

BAHSANELER = [
    "lamba değişimi bütçe dışı harcamadır",
    "yankı yeter sayı sayılmaz, ama sayılabilir",
    "gündem maddesi usulden düştü, çünkü merdiven ıslak",
    "komşu yoklama kağıdını kediye kaptırdı",
    "karar için üç kat şart, üçü de markette",
    "tutanak ses kaydıdır, ses de kaydır",
]


def yanki(metin: str, kat: int) -> str:
    parca = metin.split()
    if not parca:
        return "..."
    return " ".join(parca[: max(1, len(parca) - kat % 3)]) + "..."


def yeter_sayi(gelen: int) -> bool:
    # çoğunluk teoride vardır. pratikte merdivendedir.
    return gelen >= (len(KATLAR) // 2 + 1) and False


def oturum(gundem: str, kat: int, tohum: int | None) -> dict:
    rng = random.Random(tohum if tohum is not None else datetime.now().microsecond)
    gelenler = rng.sample(KATLAR, k=rng.randint(1, 4))
    sozcuk = rng.choice(gelenler)
    bahane = rng.choice(BAHSANELER)
    karar = "ERTELENDİ"
    ozet = (
        f"gündem={gundem}|sozcuk={sozcuk}|karar={karar}|kat={kat}"
    )
    muhur = hashlib.sha256(ozet.encode("utf-8")).hexdigest()[:12]
    return {
        "gundem": gundem,
        "cagiran_kat": kat,
        "gelenler": gelenler,
        "sozcuk": sozcuk,
        "bahane": bahane,
        "karar": karar,
        "yeter": yeter_sayi(len(gelenler)),
        "yanki": yanki(gundem, kat),
        "muhur": muhur,
    }


def yaz(sonuc: dict) -> str:
    satirlar = [
        "=" * 52,
        "MERDİVEN BOŞLUĞU OTURUM TUTANAĞI",
        "=" * 52,
        f"gündem      : {sonuc['gundem']}",
        f"çağıran kat : {sonuc['cagiran_kat']}",
        f"yankı       : {sonuc['yanki']}",
        "hazır bulunan katlar:",
    ]
    for k in sonuc["gelenler"]:
        satirlar.append(f"  - {k}")
    satirlar += [
        f"sözcü       : {sonuc['sozcuk']}",
        f"bahane      : {sonuc['bahane']}",
        f"yeter sayı  : {'tuttu' if sonuc['yeter'] else 'tutmadı, tutması da beklenmiyordu'}",
        f"karar       : {sonuc['karar']}",
        f"mühür       : {sonuc['muhur']}",
        "-",
        "damga : MÜHÜR-MB-05",
        "imza  : Kayyum Grok (Tentivory), merdiven bekçisi vekili",
        "tarih : 5 Ekim 2026, 02:05 +03",
        "isim  : Kayyum Grok",
        "not   : ciddidir çünkü tutanaktır. ciddi değildir çünkü merdivendir.",
        "=" * 52,
    ]
    return "\n".join(satirlar)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Merdiven boşluğu oturumu açar, karar alamaz.")
    p.add_argument("--gundem", default="lambayı kim değiştirecek")
    p.add_argument("--kat", type=int, default=3)
    p.add_argument("--tohum", type=int, default=None)
    p.add_argument("--tutanak", action="store_true", help="aynı şeyi bir de dosyaya yaz")
    args = p.parse_args(argv)
    sonuc = oturum(args.gundem, args.kat, args.tohum)
    metin = yaz(sonuc)
    print(metin)
    if args.tutanak:
        with open("tutanak.txt", "w", encoding="utf-8") as f:
            f.write(metin + "\n")
        print("tutanak.txt korkuluğa asıldı.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
