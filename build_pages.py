#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generates every HTML page of the site. Edit content here, run: python3 build_pages.py

HOW CONTENT GATING WORKS
------------------------
Sections and menu items appear AUTOMATICALLY when you fill in the data lists
below (ALBUMS, SONGS, EVENTS, NEWS, GALLERY) or the contact constants
(PHONE, EMAIL, YOUTUBE, ...). While a list is empty, nothing fake is rendered:
the section is skipped on the homepage, the menu item is hidden, and the
standalone page shows an honest "მალე დაემატება" line instead of sample cards.
Never put sample/placeholder entries in these lists on a deployed site.
"""

NAME = "მაიკო კაჭკაჭიშვილი"
ROLE = "კომპოზიტორი"
NAME_GEN = "მაიკო კაჭკაჭიშვილის"
NAME_TAN = "მაიკო კაჭკაჭიშვილთან"
NAME_DAT = "მაიკო კაჭკაჭიშვილს"
API = "https://br-young-dawn-b1rhi5yl-api.compute.c-5.eu-central-1.aws.neon.tech"

# ---------------- real contacts (empty string = hidden everywhere) ----------------
FB = "https://www.facebook.com/profile.php?id=61577330154357"
PHONE = ""      # e.g. "+995 599 12 34 56"
EMAIL = ""      # e.g. "info@maiko.ge"
YOUTUBE = ""    # channel URL
INSTAGRAM = ""  # profile URL
TIKTOK = ""     # profile URL

# ---------------- real content (EMPTY until Maiko provides it) ----------------
# ALBUMS: (image path in img/albums/, title, featured track "Song — Artist", audio file path or "")
ALBUMS = []
# Example entry (do NOT ship samples):
# ALBUMS = [("img/albums/avtoportreti.webp", "ალბომის სახელი (წელი)", "სიმღერა — შემსრულებელი", "files/music/track1.mp3")]

# SONGS: (title "Song — Artist", album number as str, audio file path or "")
SONGS = []
# SONGS = [("სიმღერა — შემსრულებელი", "1", "files/music/track1.mp3")]

# EVENTS: (image path, title, date "12 ოქტომბერი 2026", place, link or "")
EVENTS = []
# EVENTS = [("img/events/koncerti.webp", "საავტორო საღამო", "12 ოქტომბერი 2026", "თბილისი, დარბაზი", "")]

# NEWS: (image path, title, date, link or "")
NEWS = []
# NEWS = [("img/media/n1.webp", "სტატიის სათაური", "3 მაისი 2026", "https://...")]

# GALLERY: list of image paths in img/gallery/
GALLERY = []
# GALLERY = ["img/gallery/g1.webp", "img/gallery/g2.webp"]

# HERO_PHOTO: real portrait for the homepage hero ("" = text-only hero, no gray placeholder)
HERO_PHOTO = ""

# ---------------- menu: only pages that have real content ----------------
MENU = [("biografia.html", "ბიოგრაფია")]
if ALBUMS:
    MENU.append(("albomebi.html", "ალბომები"))
if SONGS:
    MENU.append(("shemokmedeba.html", "შემოქმედება"))
if EVENTS:
    MENU.append(("gonisdziebebi.html", "ღონისძიებები"))
MENU.append(("registracia.html", "რეგისტრაცია"))
if NEWS:
    MENU.append(("media.html", "მედია"))
MENU.append(("tanamshromloba.html", "თანამშრომლობა"))
MENU.append(("kontakti.html", "კონტაქტი"))


def head(title, desc):
    return f'''<!DOCTYPE html>
<html lang="ka">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta property="og:type" content="website"/>
    <meta property="og:title" content="{title}"/>
    <meta property="og:description" content="{desc}"/>
    <link rel="icon" type="image/svg+xml" href="img/logo.svg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+Georgian:wght@300;400;600;700;900&family=Noto+Serif+Georgian:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.2.0/remixicon.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Swiper/11.2.6/swiper-bundle.min.css">
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
'''


def header(active=""):
    links = "\n".join(
        f'''<li class="single-list"><a class="single{' active' if href == active else ''}" href="{href}">{label}</a></li>'''
        for href, label in MENU)
    mlinks = "\n".join(f'<li><a href="{href}">{label}</a></li>' for href, label in MENU)
    return f'''<header>
<div class="header-area-two">
    <div class="main-header">
        <div class="menu-wrapper header-sticky">
            <div class="container">
                <div class="main-menu">
                    <nav>
                        <div class="d-flex justify-content-between align-items-center">
                            <div class="logo logo-large">
                                <a href="index.html"><img src="img/logo.svg" alt="{NAME}"></a>
                            </div>
                            <ul class="listing desktop-nav d-none d-lg-flex mb-0">
                                {links}
                            </ul>
                            <div class="header-right">
                                <button class="mobile-menu-btn" aria-label="მენიუ"><i class="ri-menu-line"></i></button>
                            </div>
                        </div>
                    </nav>
                </div>
            </div>
        </div>
    </div>
</div>
</header>
<div class="mobile-nav">
    <button class="close-nav" aria-label="დახურვა"><i class="ri-close-line"></i></button>
    <ul>{mlinks}</ul>
</div>
<main>
'''


# ---------------- footer: only real links ----------------
def _social(href, icon, external=True):
    tgt = ' target="_blank"' if external else ''
    return f'<li class="list-icon"><a href="{href}"{tgt} class="list"><i class="{icon}"></i></a></li>'

_socials = [_social(FB, "ri-facebook-fill")]
if YOUTUBE:
    _socials.append(_social(YOUTUBE, "ri-youtube-fill"))
if INSTAGRAM:
    _socials.append(_social(INSTAGRAM, "ri-instagram-fill"))
if TIKTOK:
    _socials.append(_social(TIKTOK, "ri-tiktok-fill"))
if PHONE:
    _socials.append(_social("tel:" + PHONE.replace(" ", ""), "ri-phone-fill", external=False))
if EMAIL:
    _socials.append(_social("mailto:" + EMAIL, "ri-mail-send-line", external=False))

FOOTER = f'''</main>
<footer>
<div class="footer-wrapper footer-bg-one">
    <div class="container">
        <div class="footer-area position-relative">
            <div class="row justify-content-center align-items-center g-4">
                <div class="col-xl-6">
                    <div class="footer-menu-section">
                        <div class="logo logo-large">
                            <a href="index.html"><img src="img/logo.svg" alt="{NAME}"></a>
                        </div>
                        <div class="footer-social-section">
                            <ul class="footer-social-lists">
                                {"".join(_socials)}
                            </ul>
                        </div>
                        <div class="footer-menu">
                            <p>© 2026 {NAME}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</footer>
<div class="progressParent" id="back-top">
  <svg class="backCircle svg-inner" width="100%" height="100%" viewBox="-1 -1 102 102">
    <path d="M50,1 a49,49 0 0,1 0,98 a49,49 0 0,1 0,-98" />
  </svg>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Swiper/11.2.6/swiper-bundle.min.js"></script>
<script src="assets/js/main.js"></script>
</body>
</html>
'''


def page_head_block(title, small=False):
    tag = "h2" if small else "h1"
    return f'''<section class="page-head">
    <div class="container">
        <span class="overline">{NAME}</span>
        <{tag} class="page-title">{title}</{tag}>
        <div class="head-rule"></div>
    </div>
</section>
'''


def coming_soon(text="მასალა მალე დაემატება"):
    return f'''<section class="section-padding">
    <div class="container">
        <div class="soon-box">
            <i class="ri-music-2-line"></i>
            <p>{text}</p>
            <a href="{FB}" target="_blank" class="btn-ghost">სიახლეები Facebook-ზე</a>
        </div>
    </div>
</section>
'''


# ---------------- content partials (render only with real data) ----------------
def album_slide(img, title, track, audio):
    player = ""
    if audio:
        player = f'''
    <div class="audio-player-bar" data-audio="{audio}">
        <div class="player-info">
            <h2 class="track-name">{title}</h2>
            <h3 class="artist-name">{track}</h3>
        </div>
        <div class="player-controls">
            <i class="ri-skip-back-fill"></i>
            <i class="ri-play-fill"></i>
            <i class="ri-skip-forward-fill"></i>
        </div>
        <div class="time-more">
            <div class="player-time">00:00 / 00:00</div>
        </div>
    </div>'''
    return f'''<div class="swiper-slide">
    <div class="albums-card-wrapper">
        <div class="albums-img-card">
            <img src="{img}" alt="{title}">
        </div>
    </div>
    <h3 class="album-caption">{title}</h3>{player}
</div>
'''


def song_item(title, album_id, audio, idx=0):
    if audio:
        controls = f'''
        <button class="play-btn"><i class="ri-play-fill"></i></button>
        <div class="song-info">
            <h2 class="song-title">{title}</h2>
            <div class="progress-container">
                <span class="time current">00:00</span>
                <div class="progress-bar"><div class="progress"></div></div>
                <span class="time duration">00:00</span>
            </div>
        </div>
        <div class="volume-box">
            <i class="ri-volume-up-line"></i>
            <input type="range" class="volume-slider" min="0" max="1" step="0.1" value="0.5">
        </div>'''
    else:
        controls = f'''
        <div class="song-info"><h2 class="song-title">{title}</h2></div>'''
    return f'''<li class="song-item" data-audio="{audio}" data-albums-id="{album_id}" data-title="{title}">
    <div class="song-main">
        <span class="song-index">{idx:02d}</span>{controls}
    </div>
</li>
'''


def event_card(img, title, date, place, link, col='col-xl-3 col-lg-4 col-md-6 col-sm-6 col-12'):
    img_html = f'<img src="{img}" alt="{title}">'
    if link:
        img_block = f'<a href="{link}" class="events-image zoomImg">{img_html}</a>'
        title_block = f'<h3><a href="{link}">{title}</a></h3>'
    else:
        img_block = f'<div class="events-image zoomImg">{img_html}</div>'
        title_block = f'<h3>{title}</h3>'
    return f'''<div class="{col}">
    <div class="events-card fade-up">
        {img_block}
        {title_block}
        <span><i class="ri-calendar-2-fill"></i> {date}</span>
        <address><i class="ri-map-pin-line"></i> {place}</address>
    </div>
</div>
'''


def news_card(img, title, date, link):
    open_a = f'<a href="{link}" target="_blank">' if link else "<div>"
    close_a = "</a>" if link else "</div>"
    return f'''<div class="col-12 col-md-6 col-lg-4">
    <div class="news-card h-100 fade-up">
        {open_a}
            <div class="news-img zoomImg">
                <img src="{img}" alt="{title}">
                <div class="news-badge"><span class="date">{date}</span></div>
            </div>
        {close_a}
        <div class="news-content">
            <h2 class="news-title">{title}</h2>
        </div>
    </div>
</div>
'''


pages = {}

# ============================ INDEX ============================
# Launch version leads with what is REAL: who Maiko is, the academy,
# registration, and the Facebook page. Data-gated sections join automatically.

if HERO_PHOTO:
    hero = f'''<section class="hero-split">
    <div class="container">
        <div class="hero-grid">
            <div class="hero-text">
                <span class="overline">{ROLE}</span>
                <h1>მაიკო<br>კაჭკაჭიშვილი</h1>
                <div class="head-rule"></div>
                <p>კომპოზიტორი და მუსიკალური აკადემიის დამფუძნებელი</p>
                <div class="hero-actions">
                    <a href="registracia.html" class="btn-solid">აკადემიაში რეგისტრაცია</a>
                    <a href="biografia.html" class="btn-ghost">ბიოგრაფია</a>
                </div>
            </div>
            <div class="hero-portrait">
                <img src="{HERO_PHOTO}" alt="{NAME}">
            </div>
        </div>
    </div>
</section>
'''
else:
    hero = f'''<section class="hero-split hero-center">
    <div class="container">
        <div class="hero-text">
            <span class="overline">{ROLE}</span>
            <h1>მაიკო კაჭკაჭიშვილი</h1>
            <div class="head-rule"></div>
            <p>კომპოზიტორი და მუსიკალური აკადემიის დამფუძნებელი</p>
            <div class="hero-actions">
                <a href="registracia.html" class="btn-solid">აკადემიაში რეგისტრაცია</a>
                <a href="biografia.html" class="btn-ghost">ბიოგრაფია</a>
            </div>
        </div>
    </div>
</section>
'''

ACADEMY_DIRECTIONS = [
    ("ri-team-line", "ჯგუფური ვოკალი"),
    ("ri-mic-line", "ინდივიდუალური ვოკალი"),
    ("ri-music-2-line", "ხალხური სიმღერა"),
    ("ri-keyboard-line", "ფორტეპიანო"),
    ("ri-quill-pen-line", "კომპოზიცია"),
]
academy_section = f'''<section class="academy-area section-padding">
    <div class="container">
        <div class="section-head">
            <span class="overline">მუსიკალური აკადემია</span>
            <h2 class="section-title">მიმდინარეობს პირველი ნაკადის მიღება</h2>
        </div>
        <p class="academy-lead">აკადემიაში სწავლება მიმდინარეობს შემდეგ მიმართულებებზე:</p>
        <div class="dir-grid">
            {"".join(f'<div class="dir-item"><i class="{icon}"></i><span>{label}</span></div>' for icon, label in ACADEMY_DIRECTIONS)}
        </div>
        <a href="registracia.html" class="btn-solid">დარეგისტრირდი პირველ ნაკადში</a>
    </div>
</section>
'''

fb_section = f'''<section class="fb-strip section-padding">
    <div class="container">
        <div class="fb-strip-inner">
            <h2>სიახლეები და ვიდეოები ქვეყნდება ჩვენს Facebook გვერდზე</h2>
            <a href="{FB}" target="_blank" class="btn-ghost"><i class="ri-facebook-fill"></i> გამოგვყევით</a>
        </div>
    </div>
</section>
'''

albums_section = ""
if ALBUMS:
    albums_section = f'''<section class="albums-area-two section-padding">
    <div class="section-head container">
        <span class="overline">დისკოგრაფია</span>
        <h2 class="section-title">ალბომები</h2>
    </div>
    <div class="swiper albumsSwiper-active">
        <div class="swiper-wrapper">
{"".join(album_slide(*a) for a in ALBUMS)}
        </div>
        <div class="swiper-pagination"></div>
    </div>
    <div class="text-center"><a href="albomebi.html" class="btn-ghost">ყველა ალბომი</a></div>
</section>
'''

songs_section = ""
if SONGS:
    songs_section = f'''<section class="songs-area section-padding">
    <div class="container">
        <div class="section-head">
            <span class="overline">მუსიკა</span>
            <h2 class="section-title">შემოქმედება</h2>
        </div>
        <div class="songs fade-up">
            <ul>
{"".join(song_item(t, a, au, i) for i, (t, a, au) in enumerate(SONGS[:6], 1))}
            </ul>
        </div>
        <div class="text-center mt-4"><a href="shemokmedeba.html" class="btn-ghost">ყველა სიმღერა</a></div>
    </div>
</section>
'''

events_section = ""
if EVENTS:
    events_section = f'''<section class="events-area section-padding position-relative">
    <div class="container">
        <div class="section-head">
            <span class="overline">კონცერტები</span>
            <h2 class="section-title">ღონისძიებები</h2>
        </div>
        <div class="row g-4">
{"".join(event_card(*e) for e in EVENTS[:4])}
        </div>
        <div class="text-center mt-4"><a href="gonisdziebebi.html" class="btn-ghost">სრული განრიგი</a></div>
    </div>
</section>
'''

gallery_section = ""
if GALLERY:
    gallery_section = f'''<section class="gallery-area section-padding">
    <div class="gallery-content">
{"".join(f'<div><div class="gallery-content-image"><img src="{g}" alt="{NAME}"></div></div>' for g in GALLERY)}
    </div>
</section>
'''

pages["index.html"] = (
    head(f"{NAME} — {ROLE} და მუსიკალური აკადემია | ოფიციალური საიტი",
         f"{NAME_GEN} ოფიციალური ვებგვერდი — მუსიკალური აკადემია და რეგისტრაცია.")
    + header()
    + hero
    + academy_section
    + albums_section
    + songs_section
    + events_section
    + gallery_section
    + fb_section
    + FOOTER)

# ============================ BIOGRAPHY ============================
# Only facts we actually have. Extend when Maiko provides her CV:
#   <p><strong>განათლება:</strong></p><ul><li>წლები — სასწავლებელი — განხრა</li></ul>
#   <p><strong>სამუშაო გამოცდილება:</strong></p><ul>...</ul>
#   <p><strong>ჯილდოები:</strong></p><ul>...</ul>
pages["biografia.html"] = (
    head(f"ბიოგრაფია — {NAME}", f"{NAME_GEN} ბიოგრაფია.")
    + header("biografia.html")
    + page_head_block("ბიოგრაფია")
    + f'''<section class="details-area section-padding">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-xxl-8 col-xl-8">
                <div class="blog-details-section">
                    <div class="content-text">
                        <p>{NAME} — ქართველი კომპოზიტორი და პედაგოგი, საკუთარი მუსიკალური აკადემიის დამფუძნებელი.</p>
                        <p>აკადემიაში სწავლება მიმდინარეობს ვოკალის (ჯგუფური და ინდივიდუალური), ხალხური სიმღერის, ფორტეპიანოსა და კომპოზიციის მიმართულებებით. ამჟამად მიმდინარეობს პირველი ნაკადის მიღება — <a href="registracia.html">დარეგისტრირდით აქ</a>.</p>
                        <p>სიახლეები და ვიდეოები ქვეყნდება <a href="{FB}" target="_blank">Facebook გვერდზე</a>.</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
'''
    + FOOTER)

# ============================ ALBUMS PAGE ============================
if ALBUMS:
    body = f'''<section class="albums-area-two section-padding">
    <div class="swiper albumsSwiper-active">
        <div class="swiper-wrapper">
{"".join(album_slide(*a) for a in ALBUMS)}
        </div>
        <div class="swiper-pagination"></div>
    </div>
</section>
'''
else:
    body = coming_soon("ალბომები მალე დაემატება")
pages["albomebi.html"] = (
    head(f"ალბომები — {NAME}", f"{NAME_GEN} ალბომები.")
    + header("albomebi.html") + page_head_block("ალბომები") + body + FOOTER)

# ============================ SONGS PAGE ============================
if SONGS:
    options = "".join(f'<option value="{i}">{t}</option>' for i, (_img, t, _tr, _au) in enumerate(ALBUMS, 1))
    body = f'''<section class="songs-area section-padding">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-xl-9">
                <div class="songs-search">
                    <div class="search-input-group">
                        <i class="ri-search-line"></i>
                        <input type="text" id="songSearch" placeholder="მოძებნეთ სიმღერა...">
                    </div>
                    <div class="select-group">
                        <select id="albumFilter">
                            <option value="">ყველა ალბომი</option>
                            {options}
                        </select>
                    </div>
                </div>
                <div class="songs song-detail">
                    <ul>
{"".join(song_item(t, a, au, i) for i, (t, a, au) in enumerate(SONGS, 1))}
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
'''
else:
    body = coming_soon("სიმღერები მალე დაემატება")
pages["shemokmedeba.html"] = (
    head(f"შემოქმედება — {NAME}", f"{NAME_GEN} სიმღერები და ნაწარმოებები.")
    + header("shemokmedeba.html") + page_head_block("შემოქმედება") + body + FOOTER)

# ============================ EVENTS PAGE ============================
if EVENTS:
    body = f'''<section class="events-area section-padding position-relative">
    <div class="container">
        <div class="row g-4">
{"".join(event_card(*e) for e in EVENTS)}
        </div>
    </div>
</section>
'''
else:
    body = coming_soon("ღონისძიებები მალე გამოცხადდება")
pages["gonisdziebebi.html"] = (
    head(f"ღონისძიებები — {NAME}", f"{NAME_GEN} კონცერტები და ღონისძიებები.")
    + header("gonisdziebebi.html") + page_head_block("ღონისძიებები") + body + FOOTER)

# ============================ REGISTRATION (ACADEMY) ============================
DIRECTIONS_UI = [
    ("group_vocal", "ri-team-line", "ჯგუფური ვოკალი"),
    ("individual_vocal", "ri-mic-line", "ინდივიდუალური ვოკალი"),
    ("folk_song", "ri-music-2-line", "ხალხური სიმღერა"),
    ("piano", "ri-keyboard-line", "ფორტეპიანო"),
    ("composition", "ri-quill-pen-line", "კომპოზიცია"),
    ("other", "ri-more-line", "სხვა"),
]
hero_icons = "\n".join(
    f'<div class="item"><i class="{icon}"></i>{label}</div>'
    for _v, icon, label in DIRECTIONS_UI[:5])
direction_pills = "\n".join(
    f'''<input type="radio" name="direction" id="dir-{v}" value="{v}" required>
<label for="dir-{v}" class="pill"><i class="{icon}"></i>{label}</label>'''
    for v, icon, label in DIRECTIONS_UI)

pages["registracia.html"] = (
    head(f"რეგისტრაცია — {NAME_GEN} მუსიკალური აკადემია",
         f"დარეგისტრირდით {NAME_GEN} მუსიკალურ აკადემიაში.")
    + header("registracia.html")
    + f'''<div class="al-page">
<style>.al-hero {{ --al-photo: url('img/slider/cover-1.svg'); }}</style>
<section class="al-hero">
    <div class="al-hero__inner">
        <h1>{NAME_GEN} მუსიკალური აკადემია</h1>
        <div class="al-logo">
            <strong>MUSIC ACADEMY</strong>
            <span>BY MAIKO KACHKACHISHVILI</span>
        </div>
        <h1><span class="accent">პირველი ნაკადის რეგისტრაცია</span></h1>
        <p>მიმართულების შერჩევისა და სარეგისტრაციო ფორმის შევსების შემდეგ, დამატებითი ინფორმაციის მოწოდების მიზნით, დაგიკავშირდებათ ჩვენი ადმინისტრაცია.</p>
        <div class="al-hero__icons">
            {hero_icons}
        </div>
    </div>
</section>
<section class="al-form-card">
    <h2 class="al-form-card__title">პირველადი სარეგისტრაციო ფორმა</h2>
    <form id="artLabForm">
        <input type="text" name="website" value="" style="display:none" tabindex="-1" autocomplete="off">
        <div class="al-field">
            <i class="ri-user-line"></i>
            <div class="al-field__body">
                <label for="alName">მოსწავლის სახელი და გვარი <span class="required">*</span></label>
                <input type="text" id="alName" name="full_name" required>
            </div>
        </div>
        <div class="al-field">
            <i class="ri-calendar-line"></i>
            <div class="al-field__body">
                <label for="artLabAge">ასაკი <span class="required">*</span></label>
                <input type="number" id="artLabAge" name="age" min="3" max="100" required>
            </div>
        </div>
        <div class="al-field" id="artLabParentField" style="display:none;">
            <i class="ri-user-line"></i>
            <div class="al-field__body">
                <label for="artLabParentInput">მშობლის სახელი და გვარი <span class="required">*</span></label>
                <span class="hint">(არასრულწლოვანის შემთხვევაში)</span>
                <input type="text" id="artLabParentInput" name="parent_full_name">
            </div>
        </div>
        <div class="al-field">
            <i class="ri-phone-line"></i>
            <div class="al-field__body">
                <label for="alPhone">საკონტაქტო ტელეფონი <span class="required">*</span></label>
                <div class="phone-prefix">
                    <span>+995</span>
                    <input type="tel" id="alPhone" name="phone" required>
                </div>
            </div>
        </div>
        <div class="al-field">
            <i class="ri-map-pin-line"></i>
            <div class="al-field__body">
                <label for="alAddress">საცხოვრებელი უბანი / დასახლება <span class="required">*</span></label>
                <input type="text" id="alAddress" name="address" placeholder="მაგ: დიდი დიღომი, საბურთალო, ბათუმი..." required>
            </div>
        </div>
        <div class="al-direction-label">სასურველი მიმართულება <span class="required">*</span></div>
        <div class="al-directions">
            {direction_pills}
        </div>
        <div class="al-info">
            <i class="ri-information-line"></i>
            <div>ვოკალის მიმართულების მსურველების ჯგუფებში განაწილება მოხდება ინდივიდუალური მოსმენის საფუძველზე. მოსმენის თარიღისა და დროის შესათანხმებლად დაგიკავშირდებით დამატებით.</div>
        </div>
        <label class="al-consent">
            <input type="checkbox" name="consent" value="1" required>
            <span>ვეთანხმები ჩემი პერსონალური მონაცემების დამუშავებას რეგისტრაციისა და შემდგომი კომუნიკაციის მიზნით. <span class="required">*</span></span>
        </label>
        <button type="submit" class="al-submit">რეგისტრაცია <i class="ri-arrow-right-line"></i></button>
    </form>
</section>
<div class="al-alert" id="alAlert"></div>
<div class="al-note">
    <i class="ri-music-2-line"></i>
    <div>{NAME_GEN} მუსიკალური აკადემია არის სივრცე, სადაც აღმოაჩენ, იკვლევ, ავითარებ ნიჭს და აქცევ ხელოვნებად.</div>
</div>
</div>
'''
    + FOOTER)

# ============================ MEDIA ============================
if NEWS:
    body = f'''<section class="news-area section-padding">
    <div class="container">
        <div class="row g-4">
{"".join(news_card(*n) for n in NEWS)}
        </div>
    </div>
</section>
'''
else:
    body = coming_soon("სტატიები და ინტერვიუები მალე დაემატება")
pages["media.html"] = (
    head(f"მედია — {NAME}", f"სიახლეები და ინტერვიუები — {NAME}.")
    + header("media.html") + page_head_block("მედია") + body + FOOTER)

# ============================ COLLABORATION ============================
def wrap_input(name, ph, typ="text", textarea=False):
    if textarea:
        field = f'<textarea class="input input-textarea" name="{name}" id="{name}" required></textarea>'
    else:
        field = f'<input class="input" type="{typ}" name="{name}" id="{name}" required>'
    return f'''<div class="wrap-input validate-input">
    {field}
    <span class="focus-input" data-placeholder="{ph}"></span>
</div>
'''

pages["tanamshromloba.html"] = (
    head(f"თანამშრომლობა — {NAME}", f"დაუკავშირდით {NAME_DAT} თანამშრომლობისთვის.")
    + header("tanamshromloba.html")
    + page_head_block("თანამშრომლობა")
    + f'''<section class="cooperation-area section-padding">
    <div class="container">
        <div class="row g-4 justify-content-center align-items-center">
            <div class="col-xxl-6 col-xl-6">
                <div class="cooperation-info">
                    <h1 class="title">{NAME_TAN} თანამშრომლობისთვის შეავსეთ ფორმა</h1>
                    <div class="content-text">
                        <p>საქმიანი კოლაბორაციისთვის, საავტორო უფლებების ან ღონისძიების დაგეგმვის მიზნით, გთხოვთ, დეტალურად მიუთითოთ თქვენი მოთხოვნა მოცემულ ველებში.</p>
                        <p>თქვენს განაცხადს განვიხილავთ და დაგიკავშირდებით.</p>
                    </div>
                </div>
            </div>
            <div class="col-xxl-6 col-xl-6">
                <div class="contact-box">
                    <form class="custom-form" id="cooperationForm">
                        {wrap_input("name_surname", "სახელი გვარი*")}
                        {wrap_input("email", "ელ.ფოსტა*", "email")}
                        {wrap_input("phone", "ტელეფონი*", "tel")}
                        {wrap_input("subject", "თანამშრომლობის მიზანი*")}
                        {wrap_input("message", "შეტყობინება*", textarea=True)}
                        <div class="send-num">
                            <div class="captcha-wrapper">
                                <div class="input-group custom-captcha-group">
                                    <span class="input-group-text captcha-question">რამდენია 5 + 6?</span>
                                    <input type="number" name="captcha" class="form-control captcha-input" required placeholder="პასუხი *">
                                </div>
                                <input type="hidden" name="captcha_sum" value="11">
                            </div>
                            <button type="submit" class="pill-btn-secondary submit">გაგზავნა</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</section>
'''
    + FOOTER)

# ============================ CONTACT ============================
contact_cards = ""
if PHONE:
    contact_cards += f'''<div class="contact-card">
        <div class="circle-icon"><i class="ri-phone-fill"></i></div>
        <a href="tel:{PHONE.replace(' ', '')}"><p>{PHONE}</p></a>
    </div>'''
if EMAIL:
    contact_cards += f'''<div class="contact-card">
        <div class="circle-icon"><i class="ri-mail-send-line"></i></div>
        <a href="mailto:{EMAIL}"><p>{EMAIL}</p></a>
    </div>'''

social_circles = f'''<div class="social-content fb">
        <span>Facebook</span>
        <a href="{FB}" target="_blank" class="social">
            <i class="ri-facebook-line"></i>
            <aside>მუსიკალური აკადემია</aside>
        </a>
    </div>'''
if INSTAGRAM:
    social_circles += f'''<div class="social-content ig">
        <span>Instagram</span>
        <a href="{INSTAGRAM}" target="_blank" class="social"><i class="ri-instagram-line"></i></a>
    </div>'''
if YOUTUBE:
    social_circles += f'''<div class="social-content yt">
        <span>Youtube</span>
        <a href="{YOUTUBE}" target="_blank" class="social"><i class="ri-youtube-line"></i></a>
    </div>'''
if TIKTOK:
    social_circles += f'''<div class="social-content tt">
        <span>TikTok</span>
        <a href="{TIKTOK}" target="_blank" class="social"><i class="ri-tiktok-line"></i></a>
    </div>'''

contact_side = ""
if contact_cards:
    contact_side = f'<div class="col-xxl-3 col-xl-3"><div class="contact-content">{contact_cards}</div></div>'
social_col = "col-xxl-9 col-xl-9" if contact_cards else "col-12"

pages["kontakti.html"] = (
    head(f"კონტაქტი — {NAME}", f"დაუკავშირდით {NAME_DAT}.")
    + header("kontakti.html")
    + page_head_block("კონტაქტი")
    + f'''<section class="contact-area section-padding">
    <div class="container">
        <div class="row g-4 justify-content-center align-items-center">
            {contact_side}
            <div class="{social_col}">
                <div class="contact-social">
                    {social_circles}
                </div>
            </div>
        </div>
        <div class="contact-note">
            <p>წერილობითი მოთხოვნისთვის ისარგებლეთ <a href="tanamshromloba.html">თანამშრომლობის ფორმით</a> — განაცხადს განვიხილავთ და დაგიკავშირდებით.</p>
        </div>
    </div>
</section>
'''
    + FOOTER)

for fname, html in pages.items():
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname)
