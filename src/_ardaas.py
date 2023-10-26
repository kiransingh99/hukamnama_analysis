# ------------------------------------------------------------------------------
# _ardaas.py - Ardaas generator
#
# June 2023, Gurkiran Singh
#
# Copyright (c) 2023
# All rights reserved.
# ------------------------------------------------------------------------------

"""Handler for ardaas subparser."""

from __future__ import annotations

__all__ = ["Function", "parse"]

import argparse

import _cmn

_log = _cmn.Logger("ardaas")


def _amrit_vela(multiple: bool) -> list[str]:
    """Add lines to the ardaas to request to be woken up for amrit vela.

    :param multiple: set to True if multiple people are in the sangat.
    :return: list of lines to add to the ardaas.
    """
    return [
        f"{_pluralise('dws', multiple)} nUM sie rihq Aqy pUrw Srdw bKSo jI[ ",
        f"kl svyry nUM, kl AMimRq vyly iv~c {_pluralise('dws', multiple)} nUM AMimRq vylw iv~c jgW ky auTw ky gurbwnI pVwau[ ",
        f"{_pluralise('dws', multiple)} nUM AMimRq vylw dI dwn bKSo[ ",
    ]


def _anand_sahib() -> list[str]:
    """Add lines to the ardaas to state that 6 pauri Anand Sahib was read/sung.

    :return: list of lines to add to the ardaas.
    """
    return [
        "Cy pauVI AnMd swihb hoey[ ",
    ]


def _degh(parshaad: bool, langar: bool) -> list[str]:
    """Add lines to the ardaas to state that bhog of parshaad and/or langar was
    done.

    :param parshaad: Parshaad is present
    :param langar: Langar is present
    :return: list of lines to add to the ardaas.
    """
    anik_prakar = "Aink pRkwr Bojn bhu kIey bhu ibMjn imstwey] \
krI pwkswl soc pivqRw huix lwvhu Bogu hir rwey] "

    if parshaad and langar:
        degh = "kVwh pRswd dI dyG Aqy lMgr"
    elif parshaad:
        degh = "kVwh pRswd dI dyG"
    elif langar:
        degh = "lMgr"
    else:
        raise ValueError("Either parshaad or langar must be True")

    return [
        f"{degh} swjky hwzr hn[ ",
        anik_prakar,
        f"prvwn kIqw {degh} swD sMgq dw rsnw dy lwiek hox[ ",
        "jo jI C~ky so qyrw hI nwm jpy[ ",
    ]


def _generate(ctx: argparse.Namespace) -> None:
    """Handler for all generate requests to the Ardaas CLI.

    :param ctx: context about the original instruction.
    """
    start_unicode = ["Awp jI dy hzUr Ardws byNqI jodVI hY[ "]
    end_unicode = [
        "A~Kr vwDw Gwtw Bul cuk mwP krnI[ ",
        "srb~q dy kwrj rws krny[ ",
        "seI ipAwry myl ijnHW imilAW qyrw nwm icq Awvy[ ",
        "nwnk nwm cVHdI klw[ ",
        "qyry Bwny srb~q dw Blw[ ",
    ]

    ardaas_unicode = []

    if ctx.read_bani:
        ardaas_unicode.extend(_read_specific_banis())
    if ctx.sukhmani:
        ardaas_unicode.extend(_sukhmani())
    if ctx.kirtan:
        ardaas_unicode.extend(_kirtan())
    if ctx.anand_sahib:
        ardaas_unicode.extend(_anand_sahib())
    if ctx.sukhaasan_post:
        ardaas_unicode.extend(_sukhaasan_post())
    # For any banis that were read:
    if (
        ctx.read_bani
        or ctx.sukhmani
        or ctx.kirtan
        or ctx.anand_sahib
        or ctx.sukhaasan_post
    ):
        ardaas_unicode.extend(_read_banis(ctx.multiple))

    if ctx.katha:
        ardaas_unicode.extend(_katha())

    if ctx.akhand_paath_arambh:
        ardaas_unicode.extend(_akhand_paath_arambh())
    if ctx.akhand_paath_bhog:
        ardaas_unicode.extend(_akhand_paath_bhog())
    if ctx.sehaj_paath_arambh:
        ardaas_unicode.extend(_sehaj_paath_arambh(ctx.multiple))
    if ctx.sehaj_paath_madh:
        ardaas_unicode.extend(_sehaj_paath_madh(ctx.multiple))
    if ctx.sehaj_paath_bhog:
        ardaas_unicode.extend(_sehaj_paath_bhog(ctx.multiple))

    if ctx.birthday:
        ardaas_unicode.extend(_birthday())

    if ctx.hukamnama:
        ardaas_unicode.extend(_hukamnama(ctx.multiple))

    if ctx.parshaad or ctx.langar:
        ardaas_unicode.extend(_degh(ctx.parshaad, ctx.langar))

    if ctx.sukhaasan_pre:
        ardaas_unicode.extend(_sukhaasan_pre())

    ardaas_unicode.extend(
        [
            f"{_pluralise('Awpxy', ctx.multiple)} Axjwx {_pluralise('b~cy', ctx.multiple)} dy isr qy myhr BirAw h~Q r~Kxw[ ",
            f"{_pluralise('Awpxy', ctx.multiple)} {_pluralise('b~cy', ctx.multiple)} nUM kwm kRoD loB moh AhMkwr ausq~q inMidAw cuglIAw qoN bcwA ky r~Kxw[ ",
        ]
    )

    if ctx.amrit_vela:
        ardaas_unicode.extend(_amrit_vela(ctx.multiple))

    ardaas_unicode = start_unicode + ardaas_unicode + end_unicode
    ardaas = "".join(ardaas_unicode)

    # Now that the ardaas is fully generated, translate it
    if ctx.romanised:
        ardaas = _cmn.gurbani_unicode_to_romanised(ardaas)

    print(ardaas)


def _akhand_paath_arambh() -> list[str]:
    """Add lines to the ardaas to state that an akhand paath is about to start.

    :return: list of lines to add to the ardaas.
    """
    return [
        "Awp jI dy dwsW nUM AwigAw bKSo AKMf pwT dw AwrMBqw krn leI[ ",
    ]


def _akhand_paath_bhog() -> list[str]:
    """Add lines to the ardaas to state that an akhand paath has been done.

    :return: list of lines to add to the ardaas.
    """
    return [
        "Awp jI dy dwsW ny AKMf pwT riKAw[ ",
    ]


def _birthday() -> list[str]:
    """Add lines to the ardaas to state that today is someone's birthday.

    :return: list of lines to add to the ardaas.
    """
    return ["A~j ... dw jnmidn hY[ ", "ienUM gurisKI jIvn bKSo jI[ "]


def _hukamnama(multiple: bool) -> list[str]:
    """Add lines to the ardaas to state that a hukamnama was taken.

    :param multiple: set to True if multiple people are in the sangat.
    :return: list of lines to add to the ardaas.
    """
    jagat_jalandhaa = "jgqu jlµdw riK lY AwpxI ikrpw Dwir] \
ijqu duAwrY aubrY iqqY lYhu aubwir] \
siqguir suKu vyKwilAw scw sbdu bIcwir] \
nwnk Avru n suJeI hir ibnu bKsxhwru] "

    hukamanama_benti = f"{_pluralise('dws', multiple)} nUM awp jI dw pwvn pivqr hukmnwmw bKSo jI qy hukmnwmy dy c~lx dI smr~Qw bKSo[ "

    return [jagat_jalandhaa, hukamanama_benti]


def _katha() -> list[str]:
    """Add lines to the ardaas to state that katha was done.

    :return: list of lines to add to the ardaas.
    """
    return [
        "Awp jI dw Ak~Q k~Qw kr idAw[ ",
    ]


def _kirtan() -> list[str]:
    """Add lines to the ardaas to state that kirtan was done.

    :return: list of lines to add to the ardaas.
    """
    return [
        "Sbd kIrqn hoey[ ",
    ]


def parse(ctx: argparse.Namespace) -> None:
    """Main handler for Ardaas CLI. This is the API called by the main
    Gurbani Analysis CLI.

    :param ctx: context received from the Gurbani Analysis CLI. Namespace object
        containing the args received by the CLI.
    """
    _log.set_level(ctx.verbosity)
    _generate(ctx)

    return _cmn.RC.SUCCESS


def _pluralise(word: str, plural: bool) -> str:
    """Take in a punjabi work and return the pluralised version of it, if
    `plural` is True. Else, return the original word.

    :param word: word to pluralise.
    :param plural: whether to pluralise the word or not.
    :return: pluralised word, if `plural` is True. Else, return the original
    """
    if not plural:
        return word

    special_cases = {}

    if word in special_cases:
        return special_cases[word]

    if word[-1] == "y":
        plural = (
            word[:-2] + "i" + word[-2] + "AW"
        )  # change laav to sihaari + aera + kannaa bindi
    else:
        plural = word + "W"  # add kannaa
    return plural


def _read_banis(multiple) -> list[str]:
    """Add lines to the ardaas to state that bani was read.

    :param multiple: set to True if multiple people are in the sangat.
    """
    return [
        f"{_pluralise('dws', multiple)} ny Awp jI dy crnw kmlw pws Su~D Aqy sp~St bwnI pVI, suxI Aqy ivcwr kIqw[ ",
        "ies bwnI dw Bwv, ies bwnI dw P~l sMgqw dy ihrdy ivc vswauxw[ ",
        "bwnI pVHn, suxn Aqy ivcwr krn dy ivc AnkyW prkwr dIAw glqIAW hoieAw[ ",
        "Bul cu`k mwP krnI[ ",
    ]


def _read_specific_banis() -> list[str]:
    """Add lines to the ardaas to state that specific banis were read.

    :return: list of lines to add to the ardaas.
    """
    return ["Awp jI ... dw jwp krvwieAw[ "]


def _sehaj_paath_arambh(multiple: bool) -> list[str]:
    """Add lines to the ardaas to state that a sehaj paath raul is about to start.

    :return: list of lines to add to the ardaas.
    """
    return [
        f"Awp jI dy {_pluralise('dws', multiple)} nUM AwigAw bKSo shj pwT dw rOl dw AwrMBqw krn leI[ ",
    ]


def _sehaj_paath_madh(multiple: bool) -> list[str]:
    """Add lines to the ardaas to state that an sehaj paath raul has been done.

    :param multiple: set to True if multiple people are in the sangat.
    :return: list of lines to add to the ardaas.
    """
    return [
        f"Awp jI dy {_pluralise('dws', multiple)} ny shj pwT ivc mD ivc AweI hY[ ",
    ]


def _sehaj_paath_bhog(multiple: bool) -> list[str]:
    """Add lines to the ardaas to state that an sehaj paath raul has been done.

    :return: list of lines to add to the ardaas.
    """
    return [
        f"Awp jI dy {_pluralise('dws', multiple)} ny shj pwT dw rOl riKAw[ ",
    ]


def _sukhaasan_pre() -> list[str]:
    """Add lines to the ardaas to request permission to do sukhaasan.

    :return: list of lines to add to the ardaas.
    """
    return ["Awp jI dI suKwsn syvw krn dw AwigAw bKSnw[ "]


def _sukhaasan_post() -> list[str]:
    """Add lines to the ardaas to state that sukhaasan was done.

    :return: list of lines to add to the ardaas.
    """
    return [
        "AwigAw iml ky kIrqn soihlw dw pwT pVI geI Aqy Awp jI dI suKwsn syvw hoeI[ "
    ]


def _sukhmani() -> list[str]:
    """Add lines to the ardaas to state that Sukhmani Sahib was read.

    :return: list of lines to add to the ardaas.
    """
    sukhmani = "suKmnI suK AMimRq pRB nwmu] \
Bgq jnw kY min ibsRwm] "

    sukhmani_ardaas = "suKmnI swihb dw jwp how[ "

    return [sukhmani, sukhmani_ardaas]
