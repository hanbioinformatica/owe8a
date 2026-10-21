const counter = document.querySelector("#visit-count");
const target = Number(counter.textContent.trim());
const reduceMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
).matches;

if (Number.isSafeInteger(target) && target >= 0 && target <= 10000) {
    const formatter = new Intl.NumberFormat("nl-NL");

    if (reduceMotion) {
        counter.textContent = formatter.format(target);
    } else {
        const duration = 700;
        let startTime;

        function animateCount(timestamp) {
            startTime ??= timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            const easedProgress = 1 - (1 - progress) ** 3;

            counter.textContent = formatter.format(
                Math.round(target * easedProgress)
            );

            if (progress < 1) {
                window.requestAnimationFrame(animateCount);
            }
        }

        window.requestAnimationFrame(animateCount);
    }
}
