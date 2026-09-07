/* Maiko Kachkachishvili — site scripts */
(function () {
    "use strict";

    /* ---------- sticky header ---------- */
    const sticky = document.querySelector(".header-sticky");
    if (sticky) {
        window.addEventListener("scroll", () => {
            sticky.classList.toggle("sticky-bar", window.scrollY > 250);
        });
    }

    /* ---------- mobile menu ---------- */
    const menuBtn = document.querySelector(".mobile-menu-btn");
    const mobileNav = document.querySelector(".mobile-nav");
    if (menuBtn && mobileNav) {
        menuBtn.addEventListener("click", () => mobileNav.classList.add("open"));
        mobileNav.querySelector(".close-nav").addEventListener("click", () => mobileNav.classList.remove("open"));
        mobileNav.querySelectorAll("a").forEach(a => a.addEventListener("click", () => mobileNav.classList.remove("open")));
    }

    /* ---------- swipers ---------- */
    if (typeof Swiper !== "undefined") {
        if (document.querySelector(".heroSwiperTwo-active")) {
            new Swiper(".heroSwiperTwo-active", {
                loop: true,
                speed: 900,
                autoplay: { delay: 6000 },
                pagination: { el: ".hero-area-two .swiper-pagination", clickable: true }
            });
        }
        if (document.querySelector(".albumsSwiper-active")) {
            new Swiper(".albumsSwiper-active", {
                loop: false,
                speed: 700,
                slidesPerView: 1,
                centeredSlides: true,
                spaceBetween: 60,
                pagination: { el: ".albumsSwiper-active .swiper-pagination", clickable: true }
            });
        }
        if (document.querySelector(".eventsSwiper-active")) {
            new Swiper(".eventsSwiper-active", {
                loop: false,
                speed: 700,
                spaceBetween: 24,
                slidesPerView: 1,
                pagination: { el: ".eventsSwiper-active .swiper-pagination", clickable: true },
                breakpoints: {
                    576: { slidesPerView: 2 },
                    1200: { slidesPerView: 3 }
                }
            });
        }
    }

    /* ---------- single shared audio engine ---------- */
    const audio = new Audio();
    let currentEl = null; // element (song-item or audio-player-bar) that owns the audio

    function fmt(t) {
        if (!isFinite(t)) return "00:00";
        const m = String(Math.floor(t / 60)).padStart(2, "0");
        const s = String(Math.floor(t % 60)).padStart(2, "0");
        return m + ":" + s;
    }

    function stopCurrent() {
        if (!currentEl) return;
        audio.pause();
        const icon = currentEl.querySelector(".ri-pause-fill");
        if (icon) icon.classList.replace("ri-pause-fill", "ri-play-fill");
        currentEl = null;
    }

    /* ---------- album audio bars (vinyl players) ---------- */
    const bars = Array.from(document.querySelectorAll(".audio-player-bar"));
    bars.forEach((bar, idx) => {
        const playIcon = bar.querySelector(".player-controls .ri-play-fill, .player-controls .ri-pause-fill");
        const back = bar.querySelector(".ri-skip-back-fill");
        const fwd = bar.querySelector(".ri-skip-forward-fill");
        const timeEl = bar.querySelector(".player-time");
        if (!playIcon) return;

        playIcon.addEventListener("click", () => {
            const src = bar.dataset.audio;
            if (!src) { alert("აუდიო ფაილი ჯერ არ არის ატვირთული"); return; }
            if (currentEl === bar) {
                if (audio.paused) { audio.play(); playIcon.classList.replace("ri-play-fill", "ri-pause-fill"); }
                else { audio.pause(); playIcon.classList.replace("ri-pause-fill", "ri-play-fill"); }
                return;
            }
            stopCurrent();
            currentEl = bar;
            audio.src = src;
            audio.play();
            playIcon.classList.replace("ri-play-fill", "ri-pause-fill");
        });
        if (back) back.addEventListener("click", () => { audio.currentTime = 0; });
        if (fwd) fwd.addEventListener("click", () => {
            const next = bars[(idx + 1) % bars.length];
            const np = next.querySelector(".player-controls .ri-play-fill, .player-controls .ri-pause-fill");
            if (np) np.click();
        });
        bar._updateTime = () => {
            if (timeEl) timeEl.textContent = fmt(audio.currentTime) + " / " + fmt(audio.duration);
        };
    });

    /* ---------- song list players ---------- */
    const items = Array.from(document.querySelectorAll(".song-item"));
    items.forEach(item => {
        const btn = item.querySelector(".play-btn i");
        const progress = item.querySelector(".progress");
        const barEl = item.querySelector(".progress-bar");
        const cur = item.querySelector(".time.current");
        const dur = item.querySelector(".time.duration");
        const vol = item.querySelector(".volume-slider");
        if (!btn) return;

        item.querySelector(".play-btn").addEventListener("click", () => {
            const src = item.dataset.audio;
            if (!src) { alert("აუდიო ფაილი ჯერ არ არის ატვირთული"); return; }
            if (currentEl === item) {
                if (audio.paused) { audio.play(); btn.classList.replace("ri-play-fill", "ri-pause-fill"); }
                else { audio.pause(); btn.classList.replace("ri-pause-fill", "ri-play-fill"); }
                return;
            }
            stopCurrent();
            currentEl = item;
            audio.src = src;
            audio.play();
            btn.classList.replace("ri-play-fill", "ri-pause-fill");
        });

        if (barEl) barEl.addEventListener("click", e => {
            if (currentEl !== item || !isFinite(audio.duration)) return;
            const r = barEl.getBoundingClientRect();
            audio.currentTime = ((e.clientX - r.left) / r.width) * audio.duration;
        });
        if (vol) vol.addEventListener("input", () => {
            if (currentEl === item) audio.volume = parseFloat(vol.value);
        });
        item._updateTime = () => {
            if (progress && isFinite(audio.duration)) progress.style.width = (audio.currentTime / audio.duration * 100) + "%";
            if (cur) cur.textContent = fmt(audio.currentTime);
            if (dur) dur.textContent = fmt(audio.duration);
        };
    });

    audio.addEventListener("timeupdate", () => { if (currentEl && currentEl._updateTime) currentEl._updateTime(); });
    audio.addEventListener("loadedmetadata", () => { if (currentEl && currentEl._updateTime) currentEl._updateTime(); });
    audio.addEventListener("ended", stopCurrent);

    /* ---------- songs page: search + album filter ---------- */
    const search = document.getElementById("songSearch");
    const filter = document.getElementById("albumFilter");
    function applyFilter() {
        const q = search ? search.value.trim().toLowerCase() : "";
        const alb = filter ? filter.value : "";
        items.forEach(item => {
            const okTitle = !q || (item.dataset.title || "").toLowerCase().includes(q);
            const okAlbum = !alb || item.dataset.albumsId === alb;
            item.style.display = okTitle && okAlbum ? "" : "none";
        });
    }
    if (search) search.addEventListener("input", applyFilter);
    if (filter) filter.addEventListener("change", applyFilter);

    /* ---------- back-to-top progress circle ---------- */
    const backTop = document.getElementById("back-top");
    if (backTop) {
        const path = backTop.querySelector("path");
        const len = path.getTotalLength();
        path.style.strokeDasharray = len;
        path.style.strokeDashoffset = len;
        window.addEventListener("scroll", () => {
            const max = document.documentElement.scrollHeight - window.innerHeight;
            path.style.strokeDashoffset = len - (window.scrollY / max) * len;
            backTop.classList.toggle("rn-backto-top-active", window.scrollY > 400);
        });
        backTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
    }

    /* ---------- underline form inputs (has-val) ---------- */
    document.querySelectorAll(".wrap-input .input").forEach(inp => {
        inp.addEventListener("blur", () => inp.classList.toggle("has-val", inp.value.trim() !== ""));
    });

    /* ---------- backend API ---------- */
    const API = "https://br-young-dawn-b1rhi5yl-api.compute.c-5.eu-central-1.aws.neon.tech";

    async function apiPost(path, body) {
        const res = await fetch(API + path, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body)
        });
        return res.json();
    }

    /* ---------- cooperation form ---------- */
    const coop = document.getElementById("cooperationForm");
    if (coop) coop.addEventListener("submit", async e => {
        e.preventDefault();
        const sum = coop.querySelector('input[name="captcha_sum"]');
        const ans = coop.querySelector('input[name="captcha"]');
        if (sum && ans && ans.value.trim() !== sum.value) {
            alert("პასუხი არასწორია, სცადეთ თავიდან");
            return;
        }
        const btn = coop.querySelector('button[type="submit"]');
        btn.disabled = true;
        try {
            const data = await apiPost("/message", {
                name_surname: coop.name_surname.value,
                email: coop.email.value,
                phone: coop.phone.value,
                subject: coop.subject.value,
                message: coop.message.value
            });
            if (data.ok) {
                alert("გმადლობთ! თქვენი შეტყობინება მიღებულია. მალე დაგიკავშირდებით.");
                coop.reset();
                coop.querySelectorAll(".input").forEach(i => i.classList.remove("has-val"));
            } else {
                alert(data.error || "დაფიქსირდა შეცდომა, სცადეთ თავიდან");
            }
        } catch {
            alert("კავშირის შეცდომა — გადაამოწმეთ ინტერნეტი და სცადეთ თავიდან");
        } finally {
            btn.disabled = false;
        }
    });

    /* ---------- academy registration form ---------- */
    const lab = document.getElementById("artLabForm");
    if (lab) {
        const age = document.getElementById("artLabAge");
        const parentField = document.getElementById("artLabParentField");
        const parentInput = document.getElementById("artLabParentInput");
        const alertBox = document.getElementById("alAlert");
        function toggleParent() {
            const minor = age.value !== "" && parseInt(age.value, 10) < 18;
            parentField.style.display = minor ? "" : "none";
            if (parentInput) parentInput.required = minor;
        }
        if (age && parentField) { age.addEventListener("input", toggleParent); toggleParent(); }
        lab.addEventListener("submit", async e => {
            e.preventDefault();
            const btn = lab.querySelector('button[type="submit"]');
            btn.disabled = true;
            const dir = lab.querySelector('input[name="direction"]:checked');
            try {
                const data = await apiPost("/register", {
                    full_name: lab.full_name.value,
                    age: parseInt(lab.age.value, 10),
                    parent_full_name: parentInput ? parentInput.value : "",
                    phone: "+995 " + lab.phone.value.trim(),
                    address: lab.address.value,
                    direction: dir ? dir.value : "",
                    consent: lab.consent.checked,
                    website: lab.website ? lab.website.value : ""
                });
                if (data.ok) {
                    if (alertBox) { alertBox.className = "al-alert success"; alertBox.textContent = "გმადლობთ! თქვენი განაცხადი მიღებულია. ჩვენი ადმინისტრაცია მალე დაგიკავშირდებათ."; }
                    lab.reset();
                    toggleParent();
                } else {
                    if (alertBox) { alertBox.className = "al-alert error"; alertBox.textContent = data.error || "დაფიქსირდა შეცდომა, სცადეთ თავიდან"; }
                }
            } catch {
                if (alertBox) { alertBox.className = "al-alert error"; alertBox.textContent = "კავშირის შეცდომა — გადაამოწმეთ ინტერნეტი და სცადეთ თავიდან"; }
            } finally {
                btn.disabled = false;
                if (alertBox) alertBox.scrollIntoView({ behavior: "smooth", block: "center" });
            }
        });
    }

    /* ---------- fade-up on scroll ---------- */
    const io = new IntersectionObserver(entries => {
        entries.forEach(en => { if (en.isIntersecting) en.target.classList.add("visible"); });
    }, { threshold: .12 });
    document.querySelectorAll(".fade-up").forEach(el => io.observe(el));
})();
