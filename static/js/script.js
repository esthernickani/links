document.addEventListener('DOMContentLoaded', function() {
    /*copying shortened link to clipboard*/

    const copyBtns = document.querySelectorAll('.copy_link')
    const link = document.querySelector('.link_to_copy')

    const copyLink = async (e) => {
        e.preventDefault()
        console.log(e.target.parentElement)
        let text = e.target.parentElement.previousElementSibling.querySelector('.link_to_copy').innerText
        console.log(text)

        try {
            await navigator.clipboard.writeText(text);
            /*change text and color of button*/
            console.log(e.target.parentElement)
            e.target.parentElement.innerHTML = 'Copied!'
            console.log('Copied to clipboard')
        } catch(err) {
            console.log('Failed to copy')
        }
    }

    copyBtns.forEach(
        copyBtn => copyBtn.addEventListener('click', copyLink)
    )
    /*const submitLinkBtn = document.querySelector("#form-submit")

    async function shortenLink (e) {
        e.preventDefault();
        console.log(e)
        const baseURL = 'https://cleanuri.com/api/v1/shorten'
        const URLToBeShortened = encodeURIComponent(document.querySelector('#link').value)
        const dataToSend = {'link': URLToBeShortened}

        console.log(URLToBeShortened)
        console.log(dataToSend)
        const response = await axios.post(baseURL, dataToSend)

        console.log(response)
    }

    submitLinkBtn.addEventListener('click', shortenLink)*/
})