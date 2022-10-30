
var tooltipTriggerList
var tooltipList

const bootstrapAPI = {
    
    triggerTooltips: function() {
        tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
        tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
        console.log("TooltipList:", tooltipList)
        return tooltipTriggerList, tooltipList
    }
}

bootstrapAPI.triggerTooltips()
