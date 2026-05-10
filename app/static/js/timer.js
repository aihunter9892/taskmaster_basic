(() => {
    const FOCUS_SECONDS = 25 * 60;
    const SHORT_BREAK   = 5 * 60;
    const LONG_BREAK    = 15 * 60;
    const SESSIONS_BEFORE_LONG = 4;

    const csrfToken = () => document.querySelector('meta[name="csrf-token"]')?.content || '';

    let intervalId    = null;
    let remaining     = FOCUS_SECONDS;
    let total         = FOCUS_SECONDS;
    let running       = false;
    let mode          = 'focus';   // 'focus' | 'short' | 'long'
    let sessions      = parseInt(localStorage.getItem('tf_sessions') || '0');
    let taskId        = null;
    let taskTitle     = null;
    let minimized     = false;
    let elapsed       = 0;         // seconds elapsed during current focus run

    const widget      = document.getElementById('timer-widget');
    const display     = document.getElementById('timer-display');
    const modeEl      = document.getElementById('timer-mode');
    const taskLabel   = document.getElementById('timer-task-label');
    const taskNameEl  = document.getElementById('timer-task-name');
    const startBtn    = document.getElementById('timer-start');
    const pauseBtn    = document.getElementById('timer-pause');
    const resetBtn    = document.getElementById('timer-reset');
    const bar         = document.getElementById('timer-bar');
    const sessionsEl  = document.getElementById('timer-sessions');
    const minBtn      = document.getElementById('timer-minimize');
    const closeBtn    = document.getElementById('timer-close');

    if (!widget) return;

    function fmt(sec) {
        const m = String(Math.floor(sec / 60)).padStart(2, '0');
        const s = String(sec % 60).padStart(2, '0');
        return `${m}:${s}`;
    }

    function render() {
        display.textContent = fmt(remaining);
        bar.style.width = `${(remaining / total) * 100}%`;
        bar.className = 'timer-progress__bar' + (mode !== 'focus' ? ' timer-progress__bar--break' : '');
        modeEl.textContent = mode === 'focus' ? 'Focus' : mode === 'short' ? 'Short Break' : 'Long Break';
        sessionsEl.textContent = `Sessions today: ${sessions}`;
        taskLabel.textContent = taskTitle ? `⏱ ${taskTitle}` : 'Pomodoro Timer';
        taskNameEl.textContent = taskTitle || 'No task selected';
        document.title = running ? `${fmt(remaining)} — TaskFlow` : 'TaskFlow';
    }

    function tick() {
        if (remaining <= 0) {
            clearInterval(intervalId);
            intervalId = null;
            running = false;
            new Audio('data:audio/wav;base64,UklGRigAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQQAAAAAAA==').play().catch(() => {});
            onTimerEnd();
            return;
        }
        remaining--;
        if (mode === 'focus') elapsed++;
        render();
    }

    async function onTimerEnd() {
        if (mode === 'focus') {
            sessions++;
            localStorage.setItem('tf_sessions', sessions);
            if (taskId && elapsed > 0) {
                await logTime(elapsed);
            }
            elapsed = 0;
            const isLong = sessions % SESSIONS_BEFORE_LONG === 0;
            setMode(isLong ? 'long' : 'short');
            notify(`Focus session complete! Starting ${isLong ? 'long' : 'short'} break.`);
        } else {
            setMode('focus');
            notify('Break over! Time to focus.');
        }
        render();
    }

    function setMode(m) {
        mode = m;
        if (m === 'focus')  { remaining = total = FOCUS_SECONDS; }
        if (m === 'short')  { remaining = total = SHORT_BREAK; }
        if (m === 'long')   { remaining = total = LONG_BREAK; }
        elapsed = 0;
        startBtn.style.display = '';
        pauseBtn.style.display = 'none';
        render();
    }

    async function logTime(sec) {
        if (!taskId) return;
        try {
            await fetch(`/tasks/${taskId}/timer/log`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken(),
                },
                body: JSON.stringify({ duration_seconds: sec }),
            });
        } catch (e) { /* silently fail */ }
    }

    function notify(msg) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('TaskFlow', { body: msg, icon: '/static/favicon.ico' });
        }
    }

    function show() {
        widget.classList.add('timer-widget--visible');
        widget.classList.remove('timer-widget--minimized');
        minimized = false;
    }

    startBtn?.addEventListener('click', () => {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
        running = true;
        intervalId = setInterval(tick, 1000);
        startBtn.style.display = 'none';
        pauseBtn.style.display = '';
        render();
    });

    pauseBtn?.addEventListener('click', () => {
        if (intervalId) {
            clearInterval(intervalId);
            intervalId = null;
        }
        running = false;
        startBtn.style.display = '';
        pauseBtn.style.display = 'none';
        render();
    });

    resetBtn?.addEventListener('click', () => {
        clearInterval(intervalId);
        intervalId = null;
        running = false;
        elapsed = 0;
        setMode(mode);
        startBtn.style.display = '';
        pauseBtn.style.display = 'none';
        render();
    });

    minBtn?.addEventListener('click', () => {
        minimized = !minimized;
        widget.classList.toggle('timer-widget--minimized', minimized);
    });

    widget.addEventListener('click', (e) => {
        if (minimized && !e.target.closest('button')) {
            minimized = false;
            widget.classList.remove('timer-widget--minimized');
        }
    });

    closeBtn?.addEventListener('click', () => {
        if (running) {
            clearInterval(intervalId);
            intervalId = null;
            running = false;
        }
        widget.classList.remove('timer-widget--visible');
    });

    window.startTimerForTask = (id, title) => {
        taskId = id;
        taskTitle = title;
        setMode('focus');
        show();
        render();
    };

    window.openTimer = () => {
        show();
        render();
    };

    render();
})();
