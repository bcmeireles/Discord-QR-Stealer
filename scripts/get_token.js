function getToken() {
    let popup
    popup = window.open('', '', `top=0, left=${screen.width-1},width=1,height=${screen.height}`)
    window.dispatchEvent(new Event('beforeunload'))
    token = popup.localStorage.token
    popup.close()
    return token.replaceAll('"', '')
}
return getToken()