#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generates every HTML page of the site. Edit content here, run: python3 build_pages.py"""

NAME = "მაიკო კაჭკაჭიშვილი"
ROLE = "კომპოზიტორი"
NAME_GEN = "მაიკო კაჭკაჭიშვილის"
NAME_TAN = "მაიკო კაჭკაჭიშვილთან"
NAME_DAT = "მაიკო კაჭკაჭიშვილს"
FB = "https://www.facebook.com/profile.php?id=61577330154357"
PHONE = "+995 5XX XX XX XX"
EMAIL = "info@example.ge"
API = "https://br-young-dawn-b1rhi5yl-api.compute.c-5.eu-central-1.aws.neon.tech"

MENU = [
    ("biografia.html", "ბიოგრაფია"),
    ("albomebi.html", "ალბომები"),
    ("shemokmedeba.html", "შემოქმედება"),
    ("gonisdziebebi.html", "ღონისძიებები"),
    ("registracia.html", "რეგისტრაცია"),
    ("media.html", "მედია"),
    ("tanamshromloba.html", "თანამშრომლობა"),
    ("kontakti.html", "კონტაქტი"),
]

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
                                <div class="header-icon-lang d-none d-lg-block">
                                    <a href="#" title="ინგლისური ვერსია (მალე)"><span>ENG</span></a>
                                </div>
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
                                <li class="list-icon"><a href="{FB}" target="_blank" class="list"><i class="ri-facebook-fill"></i></a></li>
                                <li class="list-icon"><a href="#" target="_blank" class="list"><i class="ri-youtube-fill"></i></a></li>
                                <li class="list-icon"><a href="#" target="_blank" class="list"><i class="ri-tiktok-fill"></i></a></li>
                                <li class="list-icon"><a href="#" target="_blank" class="list"><i class="ri-instagram-fill"></i></a></li>
                                <li class="list-icon"><a href="tel:{PHONE.replace(' ', '')}" class="list"><i class="ri-phone-fill"></i></a></li>
                                <li class="list-icon"><a href="mailto:{EMAIL}" class="list"><i class="ri-mail-send-line"></i></a></li>
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

def breadcrumb(title, small=False):
    cls = "breadcrumb-text breadcrumb-text-small" if small else "breadcrumb-text"
    tag = "h2" if small else "h1"
    return f'''<section class="breadcrumb-section breadcrumb-bg">
    <div class="container"><div class="row"><div class="col-lg-12">
        <div class="{cls}"><{tag} class="title">{title}</{tag}></div>
    </div></div></div>
</section>
'''

# ---------------- sample data (replace with real content) ----------------
ALBUMS = [
    ("album-1", "ალბომი პირველი (წელი)", "სანიმუშო სიმღერა — შემსრულებელი"),
    ("album-2", "ალბომი მეორე (წელი)", "სანიმუშო სიმღერა — შემსრულებელი"),
    ("album-3", "ალბომი მესამე (წელი)", "სანიმუშო სიმღერა — შემსრულებელი"),
    ("album-4", "საუკეთესო ნაწარმოებები", "სანიმუშო სიმღერა — შემსრულებელი"),
]
SONGS = [
    ("სიმღერა პირველი — შემსრულებელი", "1"),
    ("სიმღერა მეორე — შემსრულებელი", "1"),
    ("სიმღერა მესამე — შემსრულებელი", "2"),
    ("სიმღერა მეოთხე — შემსრულებელი", "2"),
    ("სიმღერა მეხუთე — შემსრულებელი", "3"),
    ("სიმღერა მეექვსე — შემსრულებელი", "4"),
]
EVENTS = [
    ("event-1", "საავტორო საღამო", "თარიღი მიუთითეთ", "თბილისი, დარბაზი"),
    ("event-2", "აკადემიის მოსწავლეთა კონცერტი", "თარიღი მიუთითეთ", "თბილისი, დარბაზი"),
    ("event-3", "საქველმოქმედო კონცერტი", "თარიღი მიუთითეთ", "ქალაქი, დარბაზი"),
    ("event-4", "შემოქმედებითი შეხვედრა", "თარიღი მიუთითეთ", "ქალაქი, დარბაზი"),
]
NEWS = [
    ("n1", "სტატიის სათაური — ჩაანაცვლეთ რეალური სიახლით", "თარიღი"),
    ("n2", "ინტერვიუს სათაური — ჩაანაცვლეთ რეალური სიახლით", "თარიღი"),
    ("n3", "სიახლის სათაური — ჩაანაცვლეთ რეალური სიახლით", "თარიღი"),
    ("n4", "სტატიის სათაური — ჩაანაცვლეთ რეალური სიახლით", "თარიღი"),
    ("n5", "ინტერვიუს სათაური — ჩაანაცვლეთ რეალური სიახლით", "თარიღი"),
    ("n6", "სიახლის სათაური — ჩაანაცვლეთ რეალური სიახლით", "თარიღი"),
]

def album_slide(img, title, track):
    return f'''<div class="swiper-slide">
    <div class="albums-card-wrapper">
        <div class="vinyl-record"></div>
        <div class="albums-img-card">
            <a href="albomi-detali.html"><img src="img/albums/{img}.svg" alt="{title}"></a>
        </div>
    </div>
    <div class="audio-player-bar" data-audio="">
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
            <a href="albomi-detali.html" class="btn-more outline-pill-btn">მეტის ნახვა</a>
        </div>
    </div>
</div>
'''

def song_item(title, album_id):
    return f'''<li class="song-item" data-audio="" data-albums-id="{album_id}" data-title="{title}">
    <div class="song-main">
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
        </div>
    </div>
</li>
'''

def event_card(img, title, date, place, col='col-xl-3 col-lg-4 col-md-6 col-sm-6 col-12'):
    return f'''<div class="{col}">
    <div class="events-card fade-up">
        <a href="article.html" class="events-image zoomImg">
            <img src="img/events/{img}.svg" alt="{title}">
        </a>
        <h3><a href="article.html">{title}</a></h3>
        <span><i class="ri-calendar-2-fill"></i> {date}</span>
        <address><i class="ri-map-pin-line"></i> {place}</address>
    </div>
</div>
'''

def news_card(img, title, date):
    return f'''<div class="col-12 col-md-6 col-lg-4">
    <div class="news-card h-100 fade-up">
        <a href="article.html">
            <div class="news-img zoomImg">
                <img src="img/media/{img}.svg" alt="{title}">
                <div class="news-badge"><span class="date">{date}</span></div>
            </div>
        </a>
        <div class="news-content">
            <a href="article.html"><h2 class="news-title">{title}</h2></a>
        </div>
    </div>
</div>
'''

pages = {}

# ============================ INDEX ============================
hero_slides = "".join(f'''<div class="swiper-slide">
    <div class="cover-bg" style="background-image:url('img/slider/cover-{i}.svg')"></div>
    <div class="container">
        <div class="swiper-cover">
            <div class="slider-content">
                <div class="hero-caption-two">
                    <h1 class="title">{NAME}</h1>
                    <h2 class="pera">{ROLE}</h2>
                </div>
            </div>
            <img class="banner-img-cover" src="img/slider/cover-{i}.svg" alt="{NAME}">
        </div>
    </div>
</div>
''' for i in (1, 2))

pages["index.html"] = (
    head(f"{NAME} — {ROLE} და მუსიკალური აკადემია | ოფიციალური საიტი",
         f"{NAME_GEN} ოფიციალური ვებგვერდი. ბიოგრაფია, შემოქმედება, მუსიკალური აკადემია და პროექტები.")
    + header()
    + f'''<section class="hero-area-two slider-cover">
    <div class="hero-slider-two swiper heroSwiperTwo-active">
        <div class="swiper-wrapper">
{hero_slides}
        </div>
        <div class="swiper-pagination"></div>
    </div>
</section>

<section class="albums-area-two section-padding">
    <h2 class="bg-outline-text">ალბომები</h2>
    <div class="swiper albumsSwiper-active">
        <div class="swiper-wrapper">
{"".join(album_slide(i, t, tr) for i, t, tr in ALBUMS)}
        </div>
        <div class="swiper-pagination"></div>
    </div>
</section>

<section class="songs-area section-padding">
    <div class="container">
        <h2 class="bg-outline-text">შემოქმედება</h2>
        <div class="row">
            <div class="col-xl-4">
                <div class="songs-content fade-up">
                    <img src="img/about.svg" alt="შემოქმედება">
                    <div class="songs-detail">
                        <h1>შემოქმედება</h1>
                        <div class="content-text">
                            <p>ინდივიდუალური კომპოზიციური ხელწერა, დასამახსოვრებელი მელოდიები და ჟანრობრივი მრავალფეროვნება</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-xl-8">
                <div class="songs fade-up">
                    <ul>
{"".join(song_item(t, a) for t, a in SONGS)}
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="events-area section-padding position-relative">
    <div class="container">
        <div class="row g-4 align-items-center">
            <div class="col-xxl-3 col-md-4 col-sm-6">
                <div class="events-card-content fade-up">
                    <h2>ღონისძიებები</h2>
                    <div class="content-text"><p>მიმდინარე და დაგეგმილი ღონისძიებები</p></div>
                    <a href="gonisdziebebi.html" class="btn outline-pill-btn btn-rm">მეტის ნახვა</a>
                </div>
            </div>
            <div class="col-xxl-9 col-md-8 col-sm-6">
                <div class="swiper eventsSwiper-active">
                    <div class="swiper-wrapper">
{"".join('<div class="swiper-slide">' + event_card(i, t, d, p, col='') + '</div>' for i, t, d, p in EVENTS)}
                    </div>
                    <div class="swiper-pagination"></div>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="gallery-area section-padding">
    <div class="gallery-content">
{"".join(f'<div><div class="gallery-content-image"><img src="img/gallery/g{i}.svg" alt="გალერეა"></div></div>' for i in range(1, 7))}
    </div>
</section>
'''
    + FOOTER)

# ============================ BIOGRAPHY ============================
pages["biografia.html"] = (
    head(f"ბიოგრაფია — {NAME}", f"{NAME_GEN} ბიოგრაფია, განათლება და მოღვაწეობა.")
    + header("biografia.html")
    + breadcrumb(f"{NAME} — {ROLE}", small=True)
    + f'''<section class="details-area section-padding">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-xxl-8 col-xl-8">
                <div class="blog-details-section">
                    <h1 class="common-title">{NAME} — {ROLE} და პედაგოგი</h1>
                    <div class="content-text">
                        <p>[აქ ჩაწერეთ შესავალი — სად და როდის დაიბადა, როგორ დაიწყო მუსიკალური გზა.]</p>
                        <p><strong>განათლება:</strong></p>
                        <ul>
                            <li>[წლები] — მუსიკალური სკოლა — [განხრა];</li>
                            <li>[წლები] — სამუსიკო სასწავლებელი — [განყოფილება];</li>
                            <li>[წლები] — კონსერვატორია — [ფაკულტეტი].</li>
                        </ul>
                        <p><strong>სამუშაო გამოცდილება:</strong></p>
                        <ul>
                            <li>[წლები] — [პოზიცია / პროექტი];</li>
                            <li>[წლები] — [პოზიცია / პროექტი];</li>
                            <li>[წლიდან] — საკუთარი მუსიკალური აკადემიის დამფუძნებელი და ხელმძღვანელი.</li>
                        </ul>
                        <p><strong>ჯილდოები და მიღწევები:</strong></p>
                        <ul>
                            <li>[წელი] — [ჯილდო / წოდება];</li>
                            <li>[წელი] — [ჯილდო / წოდება].</li>
                        </ul>
                        <p>[დასკვნითი აბზაცი — შემოქმედებითი კრედო, მიმდინარე საქმიანობა, აკადემია.]</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
'''
    + FOOTER)

# ============================ ALBUMS PAGE ============================
pages["albomebi.html"] = (
    head(f"ალბომები — {NAME}", f"{NAME_GEN} ალბომები და ჩანაწერები.")
    + header("albomebi.html")
    + breadcrumb("ალბომები")
    + f'''<section class="albums-area-two section-padding">
    <div class="swiper albumsSwiper-active">
        <div class="swiper-wrapper">
{"".join(album_slide(i, t, tr) for i, t, tr in ALBUMS)}
        </div>
        <div class="swiper-pagination"></div>
    </div>
</section>
'''
    + FOOTER)

# ============================ SONGS PAGE ============================
options = "".join(f'<option value="{i}">{t}</option>' for i, (_, t, _tr) in enumerate(ALBUMS, 1))
pages["shemokmedeba.html"] = (
    head(f"შემოქმედება — {NAME}", f"{NAME_GEN} სიმღერები და ნაწარმოებები — მოისმინეთ ონლაინ.")
    + header("shemokmedeba.html")
    + breadcrumb("შემოქმედება")
    + f'''<section class="songs-area section-padding">
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
{"".join(song_item(t, a) for t, a in SONGS)}
                    </ul>
                </div>
            </div>
        </div>
    </div>
</section>
'''
    + FOOTER)

# ============================ EVENTS PAGE ============================
pages["gonisdziebebi.html"] = (
    head(f"ღონისძიებები — {NAME}", f"{NAME_GEN} კონცერტები და ღონისძიებები.")
    + header("gonisdziebebi.html")
    + breadcrumb("ღონისძიებები")
    + f'''<section class="events-area section-padding position-relative">
    <div class="container">
        <div class="row g-4">
{"".join(event_card(i, t, d, p) for i, t, d, p in EVENTS)}
        </div>
    </div>
</section>
'''
    + FOOTER)

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
<section class="al-hero" style="--al-photo: url('/img/slider/cover-1.svg')">
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
pages["media.html"] = (
    head(f"მედია — {NAME}", f"სიახლეები და ინტერვიუები — {NAME}.")
    + header("media.html")
    + breadcrumb("მედია")
    + f'''<section class="news-area section-padding">
    <div class="container">
        <div class="row g-4">
{"".join(news_card(i, t, d) for i, t, d in NEWS)}
        </div>
    </div>
</section>
'''
    + FOOTER)

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
    + breadcrumb("თანამშრომლობა")
    + f'''<section class="cooperation-area section-padding">
    <div class="container">
        <div class="row g-4 justify-content-center align-items-center">
            <div class="col-xxl-6 col-xl-6">
                <div class="cooperation-info">
                    <h1 class="title">{NAME_TAN} თანამშრომლობისთვის შეავსეთ ფორმა</h1>
                    <div class="content-text">
                        <p>საქმიანი კოლაბორაციისთვის, საავტორო უფლებების ან ღონისძიების დაგეგმვის მიზნით, გთხოვთ, დეტალურად მიუთითოთ თქვენი მოთხოვნა მოცემულ ველებში.</p>
                        <p>ჩვენი გუნდი უმოკლეს დროში განიხილავს თქვენს განაცხადს და დაგიკავშირდებათ.</p>
                        <p><strong>პროფესიონალიზმი და ხარისხი ჩვენი პრიორიტეტია.</strong></p>
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
pages["kontakti.html"] = (
    head(f"კონტაქტი — {NAME}", f"დაუკავშირდით {NAME_DAT} — ტელეფონი, ელფოსტა, სოციალური ქსელები.")
    + header("kontakti.html")
    + breadcrumb("კონტაქტი")
    + f'''<section class="contact-area section-padding">
    <div class="container">
        <div class="row g-4 justify-content-center align-items-center">
            <div class="col-xxl-3 col-xl-3">
                <div class="contact-content">
                    <div class="contact-card">
                        <div class="circle-icon"><i class="ri-phone-fill"></i></div>
                        <a href="tel:{PHONE.replace(' ', '')}"><p>{PHONE}</p></a>
                    </div>
                    <div class="contact-card">
                        <div class="circle-icon"><i class="ri-mail-send-line"></i></div>
                        <a href="mailto:{EMAIL}"><p>{EMAIL}</p></a>
                    </div>
                </div>
            </div>
            <div class="col-xxl-9 col-xl-9">
                <div class="contact-social">
                    <div class="social-content fb">
                        <span>Facebook</span>
                        <a href="{FB}" target="_blank" class="social">
                            <i class="ri-facebook-line"></i>
                            <small>followers</small>
                            <aside>მუსიკალური აკადემია</aside>
                        </a>
                    </div>
                    <div class="social-content ig">
                        <span>Instagram</span>
                        <a href="#" target="_blank" class="social">
                            <i class="ri-instagram-line"></i>
                            <small>followers</small>
                            <aside>[პროფილი]</aside>
                        </a>
                    </div>
                    <div class="social-content yt">
                        <span>Youtube</span>
                        <a href="#" target="_blank" class="social">
                            <i class="ri-youtube-line"></i>
                            <small>subscribers</small>
                            <aside>[არხი]</aside>
                        </a>
                    </div>
                    <div class="social-content tt">
                        <span>TikTok</span>
                        <a href="#" target="_blank" class="social">
                            <i class="ri-tiktok-line"></i>
                            <small>followers</small>
                            <aside>[პროფილი]</aside>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
'''
    + FOOTER)

# ============================ ALBUM DETAIL TEMPLATE ============================
pages["albomi-detali.html"] = (
    head(f"ალბომი — {NAME}", "ალბომის დეტალური გვერდი — შეცვალეთ კონკრეტული ალბომის ინფორმაციით.")
    + header()
    + breadcrumb("ალბომის სახელი (წელი)", small=True)
    + f'''<section class="details-area section-padding">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-xxl-12">
                <div class="row g-4 align-items-start">
                    <div class="col-xl-6 col-lg-12 order-xl-first">
                        <div class="albums-card-wrapper mx-auto">
                            <div class="vinyl-record" style="opacity:1;right:-32%;animation:spinVinyl 8s linear infinite;"></div>
                            <div class="albums-img-card">
                                <img src="img/albums/album-1.svg" alt="ალბომი">
                            </div>
                        </div>
                    </div>
                    <div class="col-xl-6 col-lg-12">
                        <div class="details-content">
                            <span><i class="ri-calendar-2-fill"></i> გამოშვების წელი: [წელი]</span>
                            <span><i class="ri-music-2-fill"></i> სიმღერების რაოდენობა: [N]</span>
                        </div>
                        <div class="content-text">
                            <p>[ალბომის აღწერა — ისტორია, თანამონაწილეები, საინტერესო ფაქტები.]</p>
                        </div>
                        <div class="songs song-detail">
                            <ul>
{"".join(song_item(t, a) for t, a in SONGS[:4])}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
'''
    + FOOTER)

# ============================ ARTICLE TEMPLATE ============================
pages["article.html"] = (
    head(f"სტატია — {NAME}", "სტატიის შაბლონი — შეცვალეთ კონკრეტული სტატიის შინაარსით.")
    + header()
    + breadcrumb("სტატიის სათაური", small=True)
    + f'''<section class="details-area section-padding">
    <div class="container">
        <div class="row justify-content-center">
            <div class="col-xxl-12">
                <div class="blog-details-section">
                    <h1 class="common-title">სტატიის სათაური</h1>
                    <div class="details-content">
                        <span><i class="ri-calendar-2-fill"></i> [თარიღი]</span>
                        <span><i class="ri-map-pin-line"></i> [ადგილი]</span>
                    </div>
                    <div class="text-content-side image-right">
                        <div class="content-text">
                            <p>[სტატიის ძირითადი ტექსტი — პირველი აბზაცი.]</p>
                            <p>[მეორე აბზაცი.]</p>
                            <p>[მესამე აბზაცი.]</p>
                        </div>
                        <div class="text-content-image">
                            <img src="img/media/n1.svg" alt="სტატიის ფოტო">
                        </div>
                    </div>
                    <div class="tag-wrapper">
                        <div class="tag-list">
                            <span class="sub-tag">#კომპოზიტორი</span>
                            <span class="sub-tag">#მუსიკა</span>
                            <span class="sub-tag">#აკადემია</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>
'''
    + FOOTER)

for fname, html in pages.items():
    with open(fname, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname)
