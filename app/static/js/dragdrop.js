(() => {
    const csrfToken = () => document.querySelector('meta[name="csrf-token"]').content;

    async function syncOrder() {
        const updates = [];
        document.querySelectorAll('.column__body').forEach(col => {
            const status = col.closest('.column').dataset.status;
            col.querySelectorAll('.task-card').forEach((card, index) => {
                updates.push({ id: parseInt(card.dataset.taskId), position: index, status });
            });
        });

        try {
            await fetch('/tasks/reorder', {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken() },
                body: JSON.stringify({ tasks: updates }),
            });
        } catch (e) {
            console.error('Reorder failed:', e);
        }
    }

    window.deleteTask = async (taskId) => {
        if (!confirm('Delete this task?')) return;
        try {
            const res = await fetch(`/tasks/${taskId}`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': csrfToken() },
            });
            if (res.ok) {
                const card = document.querySelector(`[data-task-id="${taskId}"]`);
                if (card) {
                    card.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
                    card.style.opacity = '0';
                    card.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        card.remove();
                        updateColumnCounts();
                        checkEmptyColumns();
                    }, 200);
                }
            }
        } catch (e) {
            console.error('Delete failed:', e);
        }
    };

    function updateColumnCounts() {
        document.querySelectorAll('.column__body').forEach(col => {
            const count = col.querySelectorAll('.task-card').length;
            const badge = col.closest('.column').querySelector('.badge');
            if (badge) badge.textContent = count;
        });
    }

    function checkEmptyColumns() {
        document.querySelectorAll('.column__body').forEach(col => {
            const existing = col.querySelector('.column__empty');
            const hasTasks = col.querySelectorAll('.task-card').length > 0;
            if (!hasTasks && !existing) {
                const empty = document.createElement('div');
                empty.className = 'column__empty';
                empty.textContent = 'Drop tasks here';
                col.appendChild(empty);
            } else if (hasTasks && existing) {
                existing.remove();
            }
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        if (typeof Sortable === 'undefined') return;

        document.querySelectorAll('.column__body').forEach(col => {
            Sortable.create(col, {
                group: 'tasks',
                animation: 150,
                ghostClass: 'sortable-ghost',
                chosenClass: 'task-card--chosen',
                onEnd: () => {
                    syncOrder();
                    updateColumnCounts();
                    checkEmptyColumns();
                },
            });
        });

        const addModal = document.getElementById('add-task-modal');
        document.querySelectorAll('[data-open-modal]').forEach(btn => {
            btn.addEventListener('click', () => addModal?.showModal());
        });

        document.getElementById('modal-close')?.addEventListener('click', () => addModal?.close());
        addModal?.addEventListener('click', e => { if (e.target === addModal) addModal.close(); });
    });
})();
