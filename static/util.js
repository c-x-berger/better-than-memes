function unix_to_pretty(date) {
    let d = new Date(date * 1000);
    const month = ("0" + (d.getMonth() + 1)).substr(-2);
    const day = ("0" + d.getDate()).substr(-2);
    return d.getFullYear() + "-" + month + "-" + day;
}

function pretty_date_element(date_element) {
    date_element.innerHTML = unix_to_pretty(date_element.innerHTML);
    date_element.classList.remove("date-unformatted");
    date_element.classList.add("date-formatted");
}

function pretty_page() {
    let x = document.getElementsByClassName("date-unformatted");
    [].forEach.call(x, pretty_date_element);
}

window.onload = pretty_page;