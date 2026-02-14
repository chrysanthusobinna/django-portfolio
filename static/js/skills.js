// ============================================
// SKILLS - Tile Picker (click to toggle)
// ============================================
(function() {
    var SKILL_CATALOGUE = {
        "Communication": [
            "Communication", "Public Speaking", "Writing",
            "Active Listening", "Presentation", "Negotiation",
            "Storytelling", "Interpersonal Skills"
        ],
        "Leadership & Management": [
            "Leadership", "Team Management", "Project Management",
            "Strategic Planning", "Decision Making", "Mentoring",
            "Conflict Resolution", "Delegation", "Change Management"
        ],
        "Problem Solving": [
            "Problem Solving", "Critical Thinking", "Data Analysis",
            "Research", "Attention to Detail", "Analytical Thinking",
            "Root Cause Analysis", "Quantitative Analysis"
        ],
        "Technical": [
            "Python", "JavaScript", "SQL", "HTML/CSS", "Java",
            "C#", "React", "Node.js", "Django", "Git",
            "AWS", "Azure", "Docker", "REST APIs", "TypeScript"
        ],
        "Business & Finance": [
            "Budgeting", "Accounting", "Financial Analysis",
            "Business Development", "Sales", "Marketing",
            "Customer Service", "Market Research", "Forecasting"
        ],
        "Office & Productivity": [
            "Microsoft Excel", "Microsoft Word", "Microsoft PowerPoint",
            "Google Workspace", "SAP", "CRM Software",
            "ERP Systems", "Typing", "Scheduling"
        ],
        "Creative & Design": [
            "Graphic Design", "UI/UX Design", "Adobe Photoshop",
            "Adobe Illustrator", "Video Editing", "Photography",
            "Content Creation", "Branding", "Figma"
        ],
        "Soft Skills": [
            "Teamwork", "Time Management", "Adaptability",
            "Creativity", "Work Ethic", "Emotional Intelligence",
            "Self-Motivation", "Resilience", "Collaboration"
        ],
        "Education & Training": [
            "Teaching", "Curriculum Development", "E-Learning",
            "Tutoring", "Coaching", "Assessment",
            "Instructional Design", "Classroom Management"
        ],
        "Digital & Social Media": [
            "Social Media", "SEO", "Content Marketing",
            "Email Marketing", "Google Analytics", "Copywriting",
            "Digital Advertising", "WordPress", "Canva"
        ]
    };

    var MAX_SKILLS = 30;
    var MAX_LENGTH = 40;
    var selected = new Set();

    var selectedBox  = document.getElementById("selectedSkillsBox");
    var skillsGrid   = document.getElementById("skillsGrid");
    var hiddenInput  = document.getElementById("skills_json");
    var categoryTabs = document.getElementById("categoryTabs");
    var warningEl    = document.getElementById("skillWarning");

    if (!selectedBox || !skillsGrid || !hiddenInput) return;

    var activeCategory = null;

    function loadFromHidden() {
        var raw = (hiddenInput.value || "").trim();
        if (!raw || raw === "[]") return;
        try {
            var parsed = JSON.parse(raw);
            if (Array.isArray(parsed)) parsed.forEach(function(s) { if (s) selected.add(String(s)); });
        } catch(e) {
            raw.split(",").forEach(function(s) { s = s.trim(); if (s) selected.add(s); });
        }
    }

    function syncHidden() {
        hiddenInput.value = JSON.stringify(Array.from(selected));
    }

    function showWarning(msg) {
        if (!warningEl) return;
        warningEl.textContent = msg;
        warningEl.classList.remove("d-none");
        clearTimeout(warningEl._t);
        warningEl._t = setTimeout(function() { warningEl.classList.add("d-none"); }, 3000);
    }

    function toggle(name) {
        if (selected.has(name)) {
            selected.delete(name);
        } else {
            if (selected.size >= MAX_SKILLS) { showWarning("Maximum " + MAX_SKILLS + " skills."); return; }
            selected.add(name);
        }
        renderChips();
        renderTiles();
        syncHidden();
    }

    function addCustom(name) {
        name = (name || "").trim().substring(0, MAX_LENGTH);
        if (!name) return false;
        var lower = name.toLowerCase();
        var dupe = false;
        selected.forEach(function(s) { if (s.toLowerCase() === lower) dupe = true; });
        if (dupe) { showWarning('"' + name + '" already added.'); return false; }
        if (selected.size >= MAX_SKILLS) { showWarning("Maximum " + MAX_SKILLS + " skills."); return false; }
        selected.add(name);
        renderChips();
        renderTiles();
        syncHidden();
        return true;
    }

    function renderChips() {
        selectedBox.innerHTML = "";
        selected.forEach(function(skill) {
            var chip = document.createElement("span");
            chip.className = "skill-chip";
            chip.innerHTML = '<span>' + skill + '</span><button type="button" class="remove-btn" aria-label="Remove ' + skill + '">\u2715</button>';
            chip.querySelector(".remove-btn").addEventListener("click", function() {
                selected.delete(skill);
                renderChips();
                renderTiles();
                syncHidden();
            });
            selectedBox.appendChild(chip);
        });
        var ph = document.createElement("span");
        ph.className = "skill-chip placeholder-chip";
        ph.textContent = selected.size ? "Add more\u2026" : "Add skill\u2026 (select below)";
        selectedBox.appendChild(ph);
    }

    function renderCategoryTabs() {
        categoryTabs.innerHTML = "";
        Object.keys(SKILL_CATALOGUE).forEach(function(cat) {
            var btn = document.createElement("button");
            btn.type = "button";
            btn.className = "skill-category-btn" + (activeCategory === cat ? " active" : "");
            btn.textContent = cat;
            btn.addEventListener("click", function() { activeCategory = cat; renderCategoryTabs(); renderTiles(); });
            categoryTabs.appendChild(btn);
        });
    }

    function renderTiles() {
        skillsGrid.innerHTML = "";
        if (!activeCategory) return;
        var cats = [activeCategory];
        cats.forEach(function(cat) {
            (SKILL_CATALOGUE[cat] || []).forEach(function(skillName) {
                var isSelected = selected.has(skillName);
                var col = document.createElement("div");
                col.className = "col-6 col-md-4 col-lg-3";
                var tile = document.createElement("div");
                tile.className = "skill-tile" + (isSelected ? " selected" : "");
                tile.setAttribute("role", "button");
                tile.setAttribute("tabindex", "0");
                tile.setAttribute("aria-pressed", isSelected ? "true" : "false");
                tile.innerHTML = '<div class="fw-semibold">' + skillName + '</div>';
                tile.addEventListener("click", function() { toggle(skillName); });
                tile.addEventListener("keydown", function(e) {
                    if (e.key === "Enter" || e.key === " ") { e.preventDefault(); toggle(skillName); }
                });
                col.appendChild(tile);
                skillsGrid.appendChild(col);
            });
        });
    }

    window.setSkills = function(arr) {
        if (!Array.isArray(arr)) return;
        selected.clear();
        arr.forEach(function(s) { addCustom(String(s)); });
    };
    window.getSkills = function() { return Array.from(selected); };

    loadFromHidden();
    renderCategoryTabs();
    renderTiles();
    renderChips();
    syncHidden();
})();
