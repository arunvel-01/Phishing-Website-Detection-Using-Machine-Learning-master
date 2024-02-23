chrome.storage.local.get(['state'], function(result) {
    var state = result.state;
    if (state === undefined) {
        state = true;
        chrome.storage.local.set({ 'state': state }, function() {});
    }
    if (state) {
        const url = window.location.toString();
        chrome.runtime.sendMessage({ URL: url });
    }
});
