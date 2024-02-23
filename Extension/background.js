chrome.runtime.onMessage.addListener(async function(request, sender) {
    console.log(request.URL, "{chrome.runtime.onMessage.addListener - request.URL}");
    if(request.URL !== ''){
        check_for_whitelist(sender, request);
    }
});

async function check_url(sender, request) {
    try {
        const response = await fetch("http://127.0.0.1:5000/", {
            method: "POST",
            body: JSON.stringify({
                url: request.URL
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        });
        if (!response.ok) {
            throw new Error("Failed to fetch data");
        }
        const result = await response.json();
        if (result.state == 1) {
            console.log("URL detected as Phishing");
            display_warning(sender, request);
            document.getElementById("result").innerText = "Phishing URL Detected";
        } else if (result.state == 0) {
            console.log("URL detected as Legitimate");
            document.getElementById("result").innerText = "Legitimate URL";
        } else {
            console.log("Error from server");
        }
    } catch (error) {
        console.error(error);
    }
}

function display_warning(sender, request) {
    let domain = new URL(request.URL).hostname;
    console.log(domain + " - domain"); 
    var warning_url = chrome.extension.getURL('phishing_warning.html') +
        '?' + sender.tab.id +
        '&' + encodeURIComponent(domain || '');
    chrome.tabs.update({'url': warning_url});
    console.log("url updated{display_warning}");
};

function check_for_whitelist(sender, request){
    let domain = new URL(request.URL).hostname;
    console.log(domain + " - domain"); 
    chrome.storage.local.get('phishing_warning_whitelist', function(result) {
        var phishingWarningWhitelist = result['phishing_warning_whitelist'];
        if (phishingWarningWhitelist != undefined && phishingWarningWhitelist[domain]) {
            console.log("Whitelisted{check_for_whitelist}");
            return;
        } else {
            console.log("Not Whitelisted{check_for_whitelist}");
            check_url(sender, request);
            return;
        }
    });
}
