(() => {
  // App State
  const state = {
    user: null,
    stream: null,
    audioContext: null,
    analyser: null,
    micSource: null,
    timerSec: 45 * 60, // 45 minutes
    timerId: null,
    current: 0,
    answers: [],
    violations: 0,
    autoSubmitAt: 5
  };

  // Elements
  const screens = {
    login: document.getElementById('screen-login'),
    consent: document.getElementById('screen-consent'),
    test: document.getElementById('screen-test'),
    result: document.getElementById('screen-result')
  };
  const statusPerms = document.getElementById('status-perms');
  const statusFullscreen = document.getElementById('status-fullscreen');
  const statusProctor = document.getElementById('status-proctor');
  const statusTimer = document.getElementById('status-timer');
  const statusViolations = document.getElementById('status-violations');
  const cameraEl = document.getElementById('camera');
  const micBar = document.getElementById('mic-level');

  const loginForm = document.getElementById('login-form');
  const agree = document.getElementById('agree');
  const btnRequest = document.getElementById('btn-request');

  const qTitle = document.getElementById('q-title');
  const qMeta = document.getElementById('q-meta');
  const qText = document.getElementById('q-text');
  const qOptions = document.getElementById('q-options');
  const btnPrev = document.getElementById('btn-prev');
  const btnNext = document.getElementById('btn-next');
  const btnSubmit = document.getElementById('btn-submit');

  const rsName = document.getElementById('rs-name');
  const rsEmail = document.getElementById('rs-email');
  const rsScore = document.getElementById('rs-score');
  const rsDetail = document.getElementById('rs-detail');
  const btnRestart = document.getElementById('btn-restart');

  // Question Bank (Electronics + Aptitude)
  const QUESTIONS = [
    { c: "Digital Electronics", q: "In a 4-bit 2’s complement system, what is the representation of -5?", options: ["1010", "1101", "1011", "0110"], a: 2, exp: "-5 = 16 - 5 = 11(dec) = 1011(2) in 4-bit 2's complement." },
    { c: "Digital Electronics", q: "The output of a NAND gate is 0 only when:", options: ["All inputs are 0", "All inputs are 1", "Any input is 0", "Inputs are different"], a: 1 },
    { c: "VLSI", q: "In CMOS, dynamic power is proportional primarily to:", options: ["Leakage current", "Short-circuit current", "C·V^2·f", "Gate length"], a: 2 },
    { c: "VLSI", q: "The channel in an NMOS forms when:", options: ["Vgs < Vth", "Vgs > Vth", "Vds > Vth", "Body is forward-biased"], a: 1 },
    { c: "DSP", q: "Nyquist rate for a signal with max freq 8 kHz is:", options: ["8 kHz", "12 kHz", "16 kHz", "32 kHz"], a: 2 },
    { c: "DSP", q: "DFT length-N has how many unique frequency samples?", options: ["N", "N/2", "N/2+1 (for real signals)", "2N"], a: 2 },
    { c: "DC (Circuits)", q: "For a resistor R, current I, power is:", options: ["I/R", "IR", "I^2R", "V/I"], a: 2 },
    { c: "DC (Circuits)", q: "KCL states that:", options: ["Voltages around a loop sum to zero", "Currents into a node sum to zero", "Power in equals power out", "Impedances add in series"], a: 1 },
    { c: "Aptitude", q: "A train 120 m long passes a pole in 6 s. Speed is:", options: ["20 m/s", "25 m/s", "18 m/s", "22 m/s"], a: 0 },
    { c: "Aptitude", q: "Simple interest on ₹5000 at 10% for 2 years:", options: ["₹500", "₹1000", "₹1500", "₹2000"], a: 1 },
    { c: "Digital Electronics", q: "Gray code differs from binary by:", options: ["Two bits per step", "No change", "One bit per step", "Random change"], a: 2 },
    { c: "DSP", q: "A causal LTI system with ROC outside outermost pole is:", options: ["Stable and causal", "Causal; stability depends on pole locations", "Always unstable", "Non-causal"], a: 1 },
    { c: "VLSI", q: "Scaling Vdd down reduces:", options: ["Dynamic power quadratically", "Dynamic power linearly", "Leakage only", "Frequency only"], a: 0 },
    { c: "DC (Circuits)", q: "Thevenin equivalent is:", options: ["Norton current source", "Single voltage source with series resistance", "Ideal current source only", "Parallel resistors only"], a: 1 },
    { c: "Aptitude", q: "If x% of 200 is 50, x is:", options: ["20", "25", "30", "35"], a: 1 }
  ];

  // Utils
  const fmtTime = (s) => {
    const m = Math.floor(s / 60).toString().padStart(2,'0');
    const r = Math.floor(s % 60).toString().padStart(2,'0');
    return `${m}:${r}`;
  };
  const switchScreen = (name) => {
    Object.values(screens).forEach(el => el.classList.remove('active'));
    screens[name].classList.add('active');
  };
  const updateBadges = () => {
    statusTimer.textContent = fmtTime(state.timerSec);
    statusViolations.textContent = `Violations: ${state.violations}`;
  };

  // Login
  loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const data = new FormData(loginForm);
    state.user = {
      name: data.get('name').trim(),
      email: data.get('email').trim(),
      roll: data.get('roll').trim()
    };
    switchScreen('consent');
  });

  // Consent
  agree.addEventListener('change', () => {
    btnRequest.disabled = !agree.checked;
  });

  btnRequest.addEventListener('click', async () => {
    try {
      await enterFullscreen();
      statusFullscreen.classList.remove('muted');
      statusFullscreen.classList.add('ok');
      statusFullscreen.textContent = 'Fullscreen On';

      await requestMedia();
      statusPerms.classList.remove('muted');
      statusPerms.classList.add('ok');
      statusPerms.textContent = 'Permitted';

      initProctoring();
      statusProctor.classList.remove('muted');
      statusProctor.classList.add('ok');
      statusProctor.textContent = 'Proctoring Active';

      startTest();
    } catch (err) {
      alert('Permissions or fullscreen were not granted. Please allow and try again.\n' + err);
    }
  });

  async function requestMedia() {
    // Get camera + mic
    state.stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    cameraEl.srcObject = state.stream;

    // Audio level meter
    state.audioContext = new (window.AudioContext || window.webkitAudioContext)();
    state.micSource = state.audioContext.createMediaStreamSource(state.stream);
    state.analyser = state.audioContext.createAnalyser();
    state.analyser.fftSize = 512;
    const data = new Uint8Array(state.analyser.frequencyBinCount);
    state.micSource.connect(state.analyser);

    const loop = () => {
      state.analyser.getByteTimeDomainData(data);
      // Simple peak detection
      let peak = 0;
      for (let i = 0; i < data.length; i++) {
        peak = Math.max(peak, Math.abs(data[i] - 128));
      }
      const level = Math.min(100, Math.floor((peak / 128) * 100));
      micBar.style.width = `${level}%`;
      requestAnimationFrame(loop);
    };
    loop();
  }

  async function enterFullscreen() {
    const el = document.documentElement;
    if (el.requestFullscreen) await el.requestFullscreen();
    else if (el.webkitRequestFullscreen) await el.webkitRequestFullscreen();
  }

  function exitFullscreen() {
    if (document.fullscreenElement) document.exitFullscreen();
    else if (document.webkitFullscreenElement) document.webkitExitFullscreen();
  }

  // Proctoring: block multitasking
  function initProctoring() {
    // Disable context menu and clipboard
    document.addEventListener('contextmenu', e => e.preventDefault());
    document.addEventListener('copy', e => e.preventDefault());
    document.addEventListener('cut', e => e.preventDefault());
    document.addEventListener('paste', e => e.preventDefault());
    // Block some keys (F12, Ctrl+Shift+I/J, Alt+Tab can't be blocked)
    document.addEventListener('keydown', (e) => {
      const k = e.key.toLowerCase();
      if (k === 'f12' || (e.ctrlKey && e.shiftKey && (k === 'i' || k === 'j')) || (e.ctrlKey && k === 's')) {
        e.preventDefault();
        e.stopPropagation();
      }
    }, true);

    // Detect tab switch / minimize / window blur
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) registerViolation('Tab/Window hidden');
    });

    window.addEventListener('blur', () => registerViolation('Window blurred'));

    // Enforce fullscreen
    document.addEventListener('fullscreenchange', () => {
      if (!document.fullscreenElement) {
        registerViolation('Exited fullscreen');
      }
    });

    // Warn before unload
    window.addEventListener('beforeunload', (e) => {
      e.preventDefault();
      e.returnValue = '';
      return '';
    });
  }

  function registerViolation(reason) {
    state.violations += 1;
    updateBadges();
    if (state.violations >= state.autoSubmitAt) {
      alert(`Violation: ${reason}\nYou reached the maximum violations. The test will be submitted.`);
      submitTest();
    } else {
      console.warn('Violation:', reason);
    }
  }

  // Test Flow
  function startTest() {
    // Initialize answers with -1 (unanswered)
    state.answers = Array(QUESTIONS.length).fill(-1);
    state.current = 0;
    switchScreen('test');
    renderQuestion();
    startTimer();
  }

  function startTimer() {
    updateBadges();
    if (state.timerId) clearInterval(state.timerId);
    state.timerId = setInterval(() => {
      state.timerSec -= 1;
      statusTimer.textContent = fmtTime(state.timerSec);
      if (state.timerSec <= 0) {
        clearInterval(state.timerId);
        alert('Time up! Submitting your test.');
        submitTest();
      }
    }, 1000);
  }

  function renderQuestion() {
    const idx = state.current;
    const item = QUESTIONS[idx];
    qTitle.textContent = `Question ${idx + 1} of ${QUESTIONS.length}`;
    qMeta.textContent = `${item.c}`;
    qText.textContent = item.q;

    qOptions.innerHTML = '';
    item.options.forEach((opt, i) => {
      const id = `opt-${idx}-${i}`;
      const wrap = document.createElement('label');
      wrap.className = 'opt';
      wrap.innerHTML = `
        <input type="radio" name="q-${idx}" id="${id}" value="${i}" ${state.answers[idx] === i ? 'checked' : ''} />
        <span>${opt}</span>
      `;
      wrap.addEventListener('click', () => {
        state.answers[idx] = i;
      });
      qOptions.appendChild(wrap);
    });

    btnPrev.disabled = idx === 0;
    btnNext.disabled = idx === QUESTIONS.length - 1;
  }

  btnPrev.addEventListener('click', () => {
    if (state.current > 0) {
      state.current -= 1;
      renderQuestion();
    }
  });

  btnNext.addEventListener('click', () => {
    if (state.current < QUESTIONS.length - 1) {
      state.current += 1;
      renderQuestion();
    }
  });

  btnSubmit.addEventListener('click', () => {
    const unanswered = state.answers.filter(a => a === -1).length;
    const ok = confirm(unanswered > 0
      ? `You have ${unanswered} unanswered question(s). Submit now?`
      : 'Submit your test now?');
    if (ok) submitTest();
  });

  function submitTest() {
    clearInterval(state.timerId);
    try { exitFullscreen(); } catch {}
    // Stop tracks
    if (state.stream) state.stream.getTracks().forEach(t => t.stop());

    // Score
    let correct = 0;
    QUESTIONS.forEach((q, i) => {
      if (state.answers[i] === q.a) correct += 1;
    });
    const score = correct;
    const total = QUESTIONS.length;

    // Show result
    rsName.textContent = `Candidate: ${state.user?.name ?? '-'}`; 
    rsEmail.textContent = `Email: ${state.user?.email ?? '-'}`;
    rsScore.textContent = `Score: ${score} / ${total}`;
    rsDetail.textContent = `Sections included: Digital Electronics, VLSI, DSP, DC (Circuits), Aptitude.`;

    // Persist minimal log locally
    const payload = {
      user: state.user,
      score,
      total,
      answers: state.answers,
      ts: new Date().toISOString(),
      violations: state.violations
    };
    try {
      localStorage.setItem('trinexial_result', JSON.stringify(payload));
    } catch {}

    switchScreen('result');
  }

  btnRestart.addEventListener('click', () => {
    window.location.reload();
  });

  // Accessibility: prevent accidental zoom and navigation
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && ['+', '-', '0', 'p'].includes(e.key.toLowerCase())) {
      e.preventDefault();
    }
    if (e.key === 'F5') {
      e.preventDefault();
    }
  }, { capture: true });

  updateBadges();
})();