const baseURL = "";
const cookies = new Cookies();

const api = axios.create({
    baseURL: baseURL
});

console.log(cookies.get("sid"));

if (cookies.get("sid") === undefined ) {
    api.logged_in = false;
} else if (cookies.get("sid") !== "null") {
    api.logged_in = true;
}

function setSid(sid) {
    cookies.set("sid", sid);
    api.defaults.headers.post["Authorization"] = sid;
    api.defaults.headers.get["Authorization"] = sid;
    api.defaults.headers.put["Authorization"] = sid;
    api.defaults.headers.delete["Authorization"] = sid;
    api.logged_in = sid !== "null" && typeof sid !== "undefined";
    console.log(api.logged_in);
}

function getCookie() {
    return cookies.get("sid");
}

function logout() {
    setSid("null");
}

export default api;
export { setSid, logout, getCookie };