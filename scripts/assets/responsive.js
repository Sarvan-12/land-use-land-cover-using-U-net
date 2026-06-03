(function() {
    function updateWidth() {
        var input = document.getElementById('viewport-width-input');
        if (input) {
            var width = window.innerWidth.toString();
            if (input.value !== width) {
                input.value = width;
                // Dispatch both input and change to trigger Dash React wrapper updates
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }
    }

    window.addEventListener('resize', updateWidth);

    // Periodically check for the input element on load
    var intervalId = setInterval(function() {
        var input = document.getElementById('viewport-width-input');
        if (input) {
            updateWidth();
            clearInterval(intervalId);
        }
    }, 100);
})();
