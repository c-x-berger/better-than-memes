function unix_to_pretty(date) {
    let d = new Date(date * 1000);
    let month = d.getMonth() + 1;
    month = month < 10 ? "0" + month : month;
    const day = d.getDate() < 10 ? "0" + d.getDate() : d.getDate();
    return d.getFullYear() + "-" + month + "-" + day;
}

function pretty_date_element(date_element) {
    date_element.innerHTML = unix_to_pretty(date_element.innerHTML);
    date_element.classList.remove("date-unformatted");
    date_element.classList.add("date-formatted");
}

function pretty_page() {
    Array.from(document.getElementsByClassName("date-unformatted")).forEach(pretty_date_element);
}

window.onload = pretty_page;