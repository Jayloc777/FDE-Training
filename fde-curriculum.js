(() => {
  const root = document.documentElement;

  const setTheme = (theme) => {
    if (theme === "light") root.setAttribute("data-theme", "light");
    else root.removeAttribute("data-theme");
    try { localStorage.setItem("fde-theme", theme); } catch (_) {}
  };

  try {
    const saved = localStorage.getItem("fde-theme");
    if (saved === "light") setTheme("light");
  } catch (_) {}

  document.querySelectorAll('[data-action="theme"]').forEach((button) => {
    button.addEventListener("click", () => {
      setTheme(root.hasAttribute("data-theme") ? "dark" : "light");
    });
  });

  document.querySelectorAll('[data-action="print"]').forEach((button) => {
    button.addEventListener("click", () => window.print());
  });

  const sidebar = document.querySelector("[data-sidebar]");
  document.querySelectorAll('[data-action="sidebar"]').forEach((button) => {
    button.addEventListener("click", () => sidebar?.classList.toggle("is-open"));
  });

  const progress = document.querySelector("[data-reading-progress]");
  const updateProgress = () => {
    if (!progress) return;
    const height = document.documentElement.scrollHeight - window.innerHeight;
    const ratio = height > 0 ? Math.min(1, Math.max(0, window.scrollY / height)) : 0;
    progress.style.width = `${ratio * 100}%`;
  };
  window.addEventListener("scroll", updateProgress, { passive: true });
  updateProgress();

  const article = document.querySelector("[data-article]");
  const toc = document.querySelector("[data-toc]");
  if (article && toc) {
    const headings = Array.from(article.querySelectorAll("h2, h3, h4"));
    if (headings.length) {
      toc.innerHTML = headings.map((heading) => {
        const level = heading.tagName.slice(1);
        return `<a class="toc-link toc-level-${level}" href="#${heading.id}">${heading.textContent}</a>`;
      }).join("");

      const links = new Map(headings.map((heading) => [heading.id, toc.querySelector(`a[href="#${heading.id}"]`)]));
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          toc.querySelectorAll(".is-current").forEach((link) => link.classList.remove("is-current"));
          links.get(entry.target.id)?.classList.add("is-current");
        });
      }, { rootMargin: "-14% 0px -72% 0px", threshold: 0 });
      headings.forEach((heading) => observer.observe(heading));
      toc.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => sidebar?.classList.remove("is-open")));
    }
  }

  const search = document.querySelector("[data-search]");
  const searchStatus = document.querySelector("[data-search-status]");
  if (search && article) {
    const blocks = Array.from(article.children);
    let statusTimer;
    const filter = () => {
      const query = search.value.trim().toLowerCase();
      let matches = 0;
      blocks.forEach((block) => {
        block.classList.remove("search-hit");
        if (!query) {
          block.classList.remove("is-search-hidden");
          return;
        }
        const found = block.textContent.toLowerCase().includes(query);
        block.classList.toggle("is-search-hidden", !found);
        if (found) { block.classList.add("search-hit"); matches += 1; }
      });
      if (!searchStatus) return;
      if (!query) {
        searchStatus.classList.remove("is-visible");
        return;
      }
      searchStatus.textContent = matches ? `找到 ${matches} 个相关内容块` : "没有找到匹配内容";
      searchStatus.classList.add("is-visible");
      window.clearTimeout(statusTimer);
      statusTimer = window.setTimeout(() => searchStatus.classList.remove("is-visible"), 2200);
    };
    search.addEventListener("input", filter);
    search.addEventListener("keydown", (event) => {
      if (event.key === "Escape") { search.value = ""; filter(); search.blur(); }
    });
  }

  const scenarioLibrary = document.querySelector("[data-scenario-library]");
  if (scenarioLibrary) {
    const grid = scenarioLibrary.querySelector("[data-scenario-grid]");
    const cards = Array.from(scenarioLibrary.querySelectorAll("[data-scenario-card]"));
    const scenarioSearch = scenarioLibrary.querySelector("[data-scenario-search]");
    const industry = scenarioLibrary.querySelector("[data-scenario-industry]");
    const difficulty = scenarioLibrary.querySelector("[data-scenario-difficulty]");
    const count = scenarioLibrary.querySelector("[data-scenario-count]");
    const empty = scenarioLibrary.querySelector("[data-scenario-empty]");
    const selectionEmpty = scenarioLibrary.querySelector("[data-scenario-selection-empty]");
    const selection = scenarioLibrary.querySelector("[data-scenario-selection]");
    const selectedMeta = scenarioLibrary.querySelector("[data-scenario-selected-meta]");
    const selectedTitle = scenarioLibrary.querySelector("[data-scenario-selected-title]");
    const selectedAssignment = scenarioLibrary.querySelector("[data-scenario-selected-assignment]");
    const selectedTasks = scenarioLibrary.querySelector("[data-scenario-selected-tasks]");
    const selectedSource = scenarioLibrary.querySelector("[data-scenario-selected-source]");

    const applyScenarioFilters = () => {
      const query = (scenarioSearch?.value || "").trim().toLowerCase();
      const industryValue = industry?.value || "";
      const difficultyValue = difficulty?.value || "";
      let visible = 0;
      cards.forEach((card) => {
        const matchesQuery = !query || card.dataset.search.toLowerCase().includes(query);
        const matchesIndustry = !industryValue || card.dataset.industry === industryValue;
        const matchesDifficulty = !difficultyValue || card.dataset.difficulty === difficultyValue;
        const matches = matchesQuery && matchesIndustry && matchesDifficulty;
        card.classList.toggle("is-search-hidden", !matches);
        if (matches) visible += 1;
      });
      if (count) count.textContent = `显示 ${visible} / ${cards.length} 个场景`;
      if (empty) empty.hidden = visible !== 0;
    };

    const chooseScenario = (card) => {
      cards.forEach((item) => item.classList.remove("is-selected"));
      card.classList.add("is-selected");
      const id = card.querySelector(".scenario-id")?.textContent || "";
      const title = card.querySelector("h3")?.textContent || "";
      const hiddenData = card.querySelector("[data-scenario-assignment]");
      const taskItems = Array.from(card.querySelectorAll(".scenario-practice-list li"));
      if (selectedMeta) selectedMeta.textContent = `${id} · ${card.dataset.industry} · ${card.dataset.difficulty}`;
      if (selectedTitle) selectedTitle.textContent = title;
      if (selectedAssignment) selectedAssignment.textContent = hiddenData?.dataset.scenarioAssignment || "";
      if (selectedTasks) {
        selectedTasks.replaceChildren(...taskItems.map((item) => {
          const li = document.createElement("li");
          li.textContent = item.textContent;
          return li;
        }));
      }
      if (selectedSource && hiddenData) {
        selectedSource.href = hiddenData.dataset.scenarioSourceUrl || "";
        selectedSource.childNodes[0].textContent = `打开首要参考来源：${hiddenData.dataset.scenarioSourceTitle || "来源"} `;
      }
      if (selectionEmpty) selectionEmpty.hidden = true;
      if (selection) selection.hidden = false;
    };

    scenarioSearch?.addEventListener("input", applyScenarioFilters);
    industry?.addEventListener("change", applyScenarioFilters);
    difficulty?.addEventListener("change", applyScenarioFilters);
    scenarioLibrary.querySelector("[data-scenario-reset]")?.addEventListener("click", () => {
      if (scenarioSearch) scenarioSearch.value = "";
      if (industry) industry.value = "";
      if (difficulty) difficulty.value = "";
      applyScenarioFilters();
    });
    grid?.addEventListener("click", (event) => {
      const button = event.target.closest("[data-scenario-select]");
      if (!button) return;
      const card = button.closest("[data-scenario-card]");
      if (card) chooseScenario(card);
    });
    applyScenarioFilters();

    const caseCards = Array.from(scenarioLibrary.querySelectorAll("[data-case-card]"));
    const caseSearch = scenarioLibrary.querySelector("[data-case-search]");
    const caseIndustry = scenarioLibrary.querySelector("[data-case-industry]");
    const caseCount = scenarioLibrary.querySelector("[data-case-count]");
    const caseEmpty = scenarioLibrary.querySelector("[data-case-empty]");
    const applyCaseFilters = () => {
      const query = (caseSearch?.value || "").trim().toLowerCase();
      const industryValue = caseIndustry?.value || "";
      let visible = 0;
      caseCards.forEach((card) => {
        const matchesQuery = !query || card.dataset.search.toLowerCase().includes(query);
        const matchesIndustry = !industryValue || card.dataset.industry === industryValue;
        const matches = matchesQuery && matchesIndustry;
        card.classList.toggle("is-search-hidden", !matches);
        if (matches) visible += 1;
      });
      if (caseCount) caseCount.textContent = "显示 " + visible + " / " + caseCards.length + " 个案例";
      if (caseEmpty) caseEmpty.hidden = visible !== 0;
    };
    caseSearch?.addEventListener("input", applyCaseFilters);
    caseIndustry?.addEventListener("change", applyCaseFilters);
    scenarioLibrary.querySelector("[data-case-reset]")?.addEventListener("click", () => {
      if (caseSearch) caseSearch.value = "";
      if (caseIndustry) caseIndustry.value = "";
      applyCaseFilters();
    });
    applyCaseFilters();
  }
})();
