#!/usr/bin/env python3
"""ВольтМаркет буклет v2 — Сайт-стиль (белый доминант), A4 landscape"""

from pptx import Presentation
from pptx.util import Pt, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import qrcode
import io

# ── Цветовая палитра (по мотивам нового сайта Figma #325) ─────────
ORANGE  = RGBColor(0xD7, 0x59, 0x45)   # фирменный оранжевый
GRAY    = RGBColor(0x7F, 0x7F, 0x7E)   # фирменный серый
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
DARK    = RGBColor(0x2C, 0x2C, 0x2B)   # тёмный (заголовки / текст)
LGRAY   = RGBColor(0xF2, 0xF2, 0xF2)   # светлые карточки (сайт-стиль)
MGRAY   = RGBColor(0xE0, 0xE0, 0xDF)   # карточки с чуть большим контрастом
MUTED   = RGBColor(0x66, 0x66, 0x65)   # вторичный текст (не белый!)
DIM     = RGBColor(0x99, 0x99, 0x98)   # третичный текст

# ── Размер A4 landscape ───────────────────────────────────────────
W = Cm(29.7)
H = Cm(21.0)

prs = Presentation()
prs.slide_width  = int(W)
prs.slide_height = int(H)
BLANK = prs.slide_layouts[6]


# ── Helpers ───────────────────────────────────────────────────────
def R(sl, x, y, w, h, fill, stroke=None, stroke_pt=1.5):
    s = sl.shapes.add_shape(1, int(x), int(y), int(w), int(h))
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if stroke:
        s.line.color.rgb = stroke
        s.line.width = Pt(stroke_pt)
    else:
        s.line.fill.background()
    return s


def T(sl, text, x, y, w, h, size, bold=False, italic=False,
      color=DARK, align=PP_ALIGN.LEFT, wrap=True):
    tb = sl.shapes.add_textbox(int(x), int(y), int(w), int(h))
    tf = tb.text_frame; tf.word_wrap = wrap
    tf.margin_left = Pt(3); tf.margin_right = Pt(3)
    tf.margin_top  = Pt(2); tf.margin_bottom = Pt(2)
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run()
    r.text = text; r.font.name = "Calibri"
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color
    return tb


def multi(sl, lines, x, y, w, h):
    tb = sl.shapes.add_textbox(int(x), int(y), int(w), int(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = Pt(4); tf.margin_right = Pt(4)
    tf.margin_top  = Pt(2); tf.margin_bottom = Pt(2)
    first = True
    for ln in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = ln.get('align', PP_ALIGN.LEFT)
        if 'sp' in ln:
            p.space_before = Pt(ln['sp'])
        r = p.add_run()
        r.text = ln.get('text', '')
        r.font.name = "Calibri"
        r.font.size = Pt(ln.get('sz', 11))
        r.font.bold = ln.get('b', False)
        r.font.italic = ln.get('i', False)
        r.font.color.rgb = ln.get('c', DARK)
    return tb


# ── QR-код (оранжевый на белом, как на сайте) ─────────────────────
qr = qrcode.QRCode(version=1,
                   error_correction=qrcode.constants.ERROR_CORRECT_H,
                   box_size=10, border=2)
qr.add_data("https://volt-market.com")
qr.make(fit=True)
qr_img = qr.make_image(fill_color=(215, 89, 69), back_color=(255, 255, 255))
qr_buf = io.BytesIO()
qr_img.save(qr_buf, "PNG")


# ══════════════════════════════════════════════════════════════════
#  СЛАЙД 1 — ЛИЦЕВАЯ СТОРОНА (сайт-стиль)
# ══════════════════════════════════════════════════════════════════
s1 = prs.slides.add_slide(BLANK)

# Белый фон — как сайт
R(s1, 0, 0, W, H, WHITE)

# Оранжевая шапка (как хедер сайта)
TBAR = Cm(1.6)
R(s1, 0, 0, W, TBAR, ORANGE)

# Серая полоска снизу
BBAR = Cm(0.5)
R(s1, 0, H - BBAR, W, BBAR, GRAY)

# ── ЛЕВАЯ ПАНЕЛЬ — обложка ────────────────────────────────────────
LW = Cm(10.5)

# Светло-серый фон левой панели (сайт-карточки)
R(s1, 0, TBAR, LW, H - TBAR - BBAR, LGRAY)

# Оранжевый блок под логотип (2/5 высоты панели — как hero-секция сайта)
HERO_H = Cm(6.5)
R(s1, 0, TBAR, LW, HERO_H, ORANGE)

# Логотип
T(s1, "ВОЛЬТ",
  Cm(0.6), Cm(1.8), LW - Cm(0.8), Cm(2.3),
  54, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
T(s1, "МАРКЕТ",
  Cm(0.6), Cm(3.9), LW - Cm(0.8), Cm(1.7),
  36, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

# Разделительная линия (белая, тонкая)
R(s1, Cm(0.6), Cm(5.85), LW - Cm(1.2), Cm(0.04), WHITE)

# ── ЛЁГКАЯ СЕРАЯ СЕКЦИЯ (как карточка на сайте) ───────────────────
# Слоган (тёмный текст на светло-сером — сайт-стиль)
T(s1, "делаем профессиональную\nэлектрику доступной",
  Cm(0.6), Cm(8.6), LW - Cm(1.0), Cm(2.2),
  12, italic=True, color=MUTED, align=PP_ALIGN.LEFT)

# Три оранжевых акцентных полосы (фирменный элемент)
for i, bw in enumerate([Cm(1.8), Cm(2.5), Cm(1.3)]):
    R(s1, Cm(0.6), Cm(11.2) + i * Cm(0.5), bw, Cm(0.3), ORANGE)

# Телефон — оранжевый блок (как CTA-кнопка сайта)
PH_Y = H - BBAR - Cm(3.7)
R(s1, Cm(0.5), PH_Y, LW - Cm(1.0), Cm(0.95), ORANGE)
T(s1, "8 800 550 11 61",
  Cm(0.5), PH_Y, LW - Cm(1.0), Cm(0.95),
  13.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
T(s1, "volt-market.com",
  Cm(0.5), PH_Y + Cm(1.05), LW - Cm(1.0), Cm(0.65),
  10, color=MUTED, align=PP_ALIGN.CENTER)
T(s1, "звонок бесплатный",
  Cm(0.5), PH_Y + Cm(1.7), LW - Cm(1.0), Cm(0.5),
  8, italic=True, color=DIM, align=PP_ALIGN.CENTER)

# ── ПРАВАЯ СЕКЦИЯ — товарные карточки (как сайт-каталог) ──────────
RX  = LW + Cm(0.25)
RW  = W - LW - Cm(0.25)

COLS  = 2
GAP_X = Cm(0.22)
GAP_Y = Cm(0.2)
PAD_X = Cm(0.28)
PAD_Y = Cm(0.28)
card_w = (RW - PAD_X * 2 - GAP_X) / COLS
card_h = (H - TBAR - BBAR - PAD_Y * 2 - GAP_Y * 2) / 3

products = [
    ("РОЗЕТКИ И\nВЫКЛЮЧАТЕЛИ",   "Надёжные решения для вашего дома"),
    ("СВЕТИЛЬНИКИ\nНА ШИНОПРОВОД", "Современное трековое освещение"),
    ("СВЕТОДИОДНАЯ\nЛЕНТА",        "Яркий свет — низкое энергопотребление"),
    ("КАБЕЛЬ ВВГ\n(синий)",         "Силовые кабели высшего качества"),
    ("АВТОМАТЫ\nCHINT",            "Надёжная защита вашей электросети"),
]

for i, (name, desc) in enumerate(products):
    col = i % COLS
    row = i // COLS
    cx = RX + PAD_X + col * (card_w + GAP_X)
    cy = TBAR + PAD_Y + row * (card_h + GAP_Y)

    # Карточка — светло-серая, как на сайте
    R(s1, cx, cy, card_w, card_h, LGRAY)
    # Оранжевая полоска сверху (сайт-стиль: hover-акцент)
    R(s1, cx, cy, card_w, Cm(0.25), ORANGE)
    # Название
    T(s1, name,
      cx + Cm(0.25), cy + Cm(0.38), card_w - Cm(0.5), card_h * 0.50,
      10, bold=True, color=DARK)
    # Описание
    T(s1, desc,
      cx + Cm(0.25), cy + card_h * 0.54, card_w - Cm(0.5), card_h * 0.40,
      8.5, color=MUTED)

# 6-я ячейка — CTA (оранжевый, как кнопка «В корзину» на сайте)
col, row = 1, 2
cx = RX + PAD_X + col * (card_w + GAP_X)
cy = TBAR + PAD_Y + row * (card_h + GAP_Y)
R(s1, cx, cy, card_w, card_h, ORANGE)
T(s1, "СКИДКА\nДО 15%",
  cx + Cm(0.25), cy + Cm(0.3), card_w - Cm(0.5), card_h * 0.58,
  20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
T(s1, "покажите этот буклет\nв любом магазине",
  cx + Cm(0.25), cy + card_h * 0.63, card_w - Cm(0.5), card_h * 0.32,
  8.5, italic=True, color=WHITE, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════════════════
#  СЛАЙД 2 — ОБОРОТНАЯ СТОРОНА + КУПОН (белый, как страницы сайта)
# ══════════════════════════════════════════════════════════════════
s2 = prs.slides.add_slide(BLANK)

# Белый фон
R(s2, 0, 0, W, H, WHITE)
# Оранжевый хедер
R(s2, 0, 0, W, TBAR, ORANGE)
# Серый футер
R(s2, 0, H - BBAR, W, BBAR, GRAY)

# Вертикальный разделитель между блоками
INFO_W = W * 0.615
R(s2, INFO_W - Cm(0.01), TBAR, Cm(0.02), H - TBAR - BBAR, MGRAY)

# ── ЛЕВЫЙ БЛОК ────────────────────────────────────────────────────

# Заголовок «Наши магазины» (как h2 на сайте)
T(s2, "НАШИ МАГАЗИНЫ",
  Cm(0.7), Cm(2.0), Cm(14), Cm(1.05),
  18, bold=True, color=DARK)
# Оранжевая подчёркивающая линия заголовка (брендинг-элемент)
R(s2, Cm(0.7), Cm(3.1), Cm(3.2), Cm(0.07), ORANGE)

stores = [
    ("г. Оренбург", "пр. Победы, 151"),
    ("г. Оренбург", "пр. Автоматики, 28А"),
    ("г. Орск",     "пр. Ленина, 95А"),
]
each_w = (INFO_W - Cm(1.2)) / 3 - Cm(0.2)
for i, (city, addr) in enumerate(stores):
    sx = Cm(0.5) + i * (each_w + Cm(0.2))
    sy = Cm(3.4)
    # Белая карточка с лёгкой рамкой (сайт-карточка)
    R(s2, sx, sy, each_w, Cm(3.0), LGRAY)
    # Оранжевый левый акцент
    R(s2, sx, sy, Cm(0.2), Cm(3.0), ORANGE)
    T(s2, city,
      sx + Cm(0.35), sy + Cm(0.2), each_w - Cm(0.45), Cm(0.65),
      10.5, bold=True, color=ORANGE)
    T(s2, addr,
      sx + Cm(0.35), sy + Cm(0.9), each_w - Cm(0.45), Cm(0.9),
      9.5, color=DARK, wrap=True)
    T(s2, "Пн–Вс: 9:00–20:00",
      sx + Cm(0.35), sy + Cm(1.85), each_w - Cm(0.45), Cm(0.55),
      8, italic=True, color=DIM)
    T(s2, "электротовары / освещение",
      sx + Cm(0.35), sy + Cm(2.45), each_w - Cm(0.45), Cm(0.45),
      7.5, color=DIM)

# Телефон (крупный, как на странице контактов сайта)
T(s2, "8 800 550 11 61",
  Cm(0.7), Cm(7.1), Cm(10), Cm(1.05),
  24, bold=True, color=ORANGE)
T(s2, "звонок бесплатный  |  volt-market.com",
  Cm(0.7), Cm(8.15), Cm(13), Cm(0.6),
  9, italic=True, color=DIM)

# Заголовок «Почему выбирают нас»
T(s2, "ПОЧЕМУ ВЫБИРАЮТ НАС",
  Cm(0.7), Cm(9.1), Cm(14), Cm(0.85),
  13, bold=True, color=DARK)
R(s2, Cm(0.7), Cm(9.95), Cm(2.8), Cm(0.06), ORANGE)

benefits = [
    "Широкий ассортимент электротоваров",
    "Профессиональные консультации бесплатно",
    "Цены от производителя — без наценок",
    "Только проверенные бренды и сертификаты",
    "Гарантия на все товары",
]
for i, b in enumerate(benefits):
    bx = Cm(0.7)
    by = Cm(10.25) + i * Cm(0.98)
    # Оранжевый бейдж (сайт: иконка-маркер)
    R(s2, bx, by + Cm(0.06), Cm(0.52), Cm(0.52), ORANGE)
    T(s2, "✓",
      bx + Cm(0.04), by - Cm(0.02), Cm(0.52), Cm(0.62),
      9.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    T(s2, b, bx + Cm(0.68), by, Cm(12), Cm(0.62), 9.5, color=MUTED)

# Статистика (три блока — как цифровые акценты на лендинге сайта)
STAT_Y = Cm(15.6)
stats = [
    ("11 000+", "наименований\nсветильников"),
    ("3 000+",  "моделей розеток\nи выключателей"),
    ("100%",    "оригинальные\nтовары"),
]
stat_w = (INFO_W - Cm(1.0)) / 3
for i, (num, lbl) in enumerate(stats):
    stx = Cm(0.5) + i * stat_w
    R(s2, stx + Cm(0.06), STAT_Y, stat_w - Cm(0.12), Cm(2.7), LGRAY)
    # Оранжевая верхняя полоска (сайт-карточка)
    R(s2, stx + Cm(0.06), STAT_Y, stat_w - Cm(0.12), Cm(0.2), ORANGE)
    T(s2, num,
      stx, STAT_Y + Cm(0.25), stat_w, Cm(1.15),
      22, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    T(s2, lbl,
      stx, STAT_Y + Cm(1.45), stat_w, Cm(1.1),
      8, italic=True, color=DIM, align=PP_ALIGN.CENTER)

# Слоган внизу
T(s2, "«Вместе создаём светлое будущее»",
  Cm(0.7), H - BBAR - Cm(1.65), Cm(14), Cm(0.65),
  9.5, italic=True, color=DIM)

# ── ПРАВЫЙ БЛОК — QR + Купон ──────────────────────────────────────
RQX = INFO_W + Cm(0.25)
RQW = W - RQX - Cm(0.35)

# Подпись к QR
T(s2, "Сканируйте — узнайте цены\nи ассортимент прямо сейчас",
  RQX, Cm(2.0), RQW, Cm(1.1),
  9.5, color=MUTED, align=PP_ALIGN.CENTER)

# QR-код
qr_buf.seek(0)
QR_SZ = Cm(5.0)
s2.shapes.add_picture(qr_buf,
                      int(RQX + (RQW - QR_SZ) / 2),
                      int(Cm(3.2)),
                      int(QR_SZ), int(QR_SZ))
T(s2, "volt-market.com",
  RQX, Cm(8.45), RQW, Cm(0.7),
  11, bold=True, color=DARK, align=PP_ALIGN.CENTER)

# ── КУПОН (как pop-up блок на сайте) ──────────────────────────────
CPX = RQX
CPY = Cm(9.45)
CPW = RQW
CPH = H - CPY - BBAR - Cm(0.35)

# Фон купона — светло-серый
R(s2, CPX, CPY, CPW, CPH, LGRAY)
# Оранжевая шапка купона
CHDR = Cm(1.1)
R(s2, CPX, CPY, CPW, CHDR, ORANGE)
T(s2, "КУПОН НА СКИДКУ",
  CPX + Cm(0.2), CPY + Cm(0.1), CPW - Cm(0.4), CHDR - Cm(0.1),
  12.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# Большая скидка (оранжевый акцент)
T(s2, "ДО 15%",
  CPX + Cm(0.2), CPY + CHDR + Cm(0.15),
  CPW - Cm(0.4), Cm(1.85),
  42, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

# Пояснение
multi(s2, [
    {'text': "скидка на любой товар",
     'sz': 9.5, 'c': MUTED, 'align': PP_ALIGN.CENTER},
    {'text': "при предъявлении этого буклета",
     'sz': 9.5, 'c': MUTED, 'align': PP_ALIGN.CENTER, 'sp': 1},
], CPX + Cm(0.2), CPY + CHDR + Cm(2.1), CPW - Cm(0.4), Cm(1.0))

# Доп. бонус — белая карточка (сайт-стиль)
R(s2, CPX + Cm(0.4), CPY + CHDR + Cm(3.2), CPW - Cm(0.8), Cm(0.72), WHITE)
T(s2, "Бесплатная консультация электрика",
  CPX + Cm(0.4), CPY + CHDR + Cm(3.2), CPW - Cm(0.8), Cm(0.72),
  8.5, color=DARK, align=PP_ALIGN.CENTER)

# Условия
T(s2, "* Не суммируется с другими акциями.\nДействителен до 31.12.2026",
  CPX + Cm(0.3), CPY + CPH - Cm(0.95), CPW - Cm(0.6), Cm(0.85),
  6.5, italic=True, color=DIM, align=PP_ALIGN.CENTER)


# ── Сохранение ────────────────────────────────────────────────────
OUT = r"D:\Desktop\ИИ\МЫСЛИ ПРОЕКТ ИИ\Буклет_ВольтМаркет_v2.pptx"
prs.save(OUT)
print("OK:", OUT)
