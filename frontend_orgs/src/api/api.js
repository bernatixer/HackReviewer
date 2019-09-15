import axios from "axios";
import Cookies from "universal-cookie";

const cookies = new Cookies();

const baseURL = "https://htn.oriolclosa.dev/api/v1.0/";

const api = axios.create({
    baseURL: baseURL
});

console.log(cookies.get("sid"));

if (cookies.get("sid") === undefined ) {
    api.logged_in = false;
} else if (cookies.get("sid") !== "null") {
    api.logged_in = true;
}

api.logged_in = false;

let sid = cookies.get("sid");
if (sid) setSid(sid);

function setUsername(username) {
    cookies.set("username", username, { path: "/" });
}

function setEmail(email) {
    cookies.set("email", email, { path: "/" });
}

function setSid(sid) {
    cookies.set("sid", sid, { path: "/" });
    api.defaults.headers.post["Authorization"] = sid;
    api.defaults.headers.get["Authorization"] = sid;
    api.defaults.headers.put["Authorization"] = sid;
    api.defaults.headers.delete["Authorization"] = sid;
    api.logged_in = sid !== "null" && typeof sid !== "undefined";
}

function setAccess(access) {
    cookies.set("access", access, {path: "/"});
}

function getAccess() {
    return cookies.get("access");
}

function getUsername() {
    return cookies.get("username");
}

function getEmail() {
    return cookies.get("email");
}

function logout() {
    setSid("null");
    setUsername("");
    setEmail("");
    setAccess("");
}

export default api;
export { setSid, setUsername, getUsername, logout, setEmail, getEmail, setAccess, getAccess };
