
// substitute view and modify tokens to direct URL links
document.addEventListener("DOMContentLoaded", () => {
    for (let elementId of ["share-view", "share-modify"]) {
        const element = document.querySelector(`#${elementId}`)
        if (element === null) continue
        element.value = `${location.origin}/paste/${element.value}`
    }
})

/**
 * @param {string} elementId Input element whose value to copy to clipboard.
 */
const copyInput = elementId => {
    const value = document.querySelector(`#${elementId}`).value
    navigator.clipboard.writeText(value)
        .then(() => alert("Copied!"))
        .catch(() => alert("Copying failed."))
}
