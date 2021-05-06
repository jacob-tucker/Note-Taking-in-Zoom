function onOpen() {
  var ui = DocumentApp.getUi();

  // sets a global variable "started" to false
  PropertiesService.getDocumentProperties().setProperty('started', 'false')
  
  // Adds a button at the top called Record
  ui.createMenu('Record')
    .addItem('Open Sidebar', 'openSidebar')
    .addToUi();
}

function openSidebar() {
  var html = HtmlService.createHtmlOutputFromFile('Index');
  DocumentApp.getUi()
      .showSidebar(html);
}

function recordTimestamp() {
  
  // Gets the current time
  var d = new Date();
  var timeStamp = d.toLocaleTimeString();

  // Gets the document's body
  var body = DocumentApp.getActiveDocument().getBody();
  let started = PropertiesService.getDocumentProperties().getProperty('started');

  var document = DocumentApp.getActiveDocument();
  var cursor = document.getCursor().getElement();
  var childIndex  = cursor.getParent().getChildIndex(cursor);
  if (started == 'false') {
    var ui = DocumentApp.getUi();

    var result = ui.prompt(
        'Your Section Title',
        ui.ButtonSet.OK_CANCEL);

    // Process the user's response.
    var button = result.getSelectedButton();
    var text = result.getResponseText();
    if (button == ui.Button.OK) {
      // User clicked "OK".
      var startedPar = body.insertParagraph(childIndex, "# " + text + ": " + timeStamp);
      startedPar.setHeading(DocumentApp.ParagraphHeading.HEADING3);
      PropertiesService.getDocumentProperties().setProperty('started', 'true');
    }
  } else if (started == 'true') {
    body.insertParagraph(childIndex, "# stop: " + timeStamp);
    PropertiesService.getDocumentProperties().setProperty('started', 'false');
  }
  
}