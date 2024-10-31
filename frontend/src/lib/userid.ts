import { browser } from "$app/environment";

function generateAndSetUUID() {
    const userid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
    localStorage.setItem('userid', userid);
    return userid;
}

export const userid = browser ? (localStorage.getItem('userid') || generateAndSetUUID()) : undefined;
