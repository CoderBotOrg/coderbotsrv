export class BlocklyWorkspace {
  constructor (workspace_id, toolbox_id) {
    this.workspace = Blockly.inject(document.getElementById(workspace_id),
      {path: '../../', toolbox: document.getElementById(toolbox_id),
      scrollbars: true, maxBlocks: -1})
  }

  load (xml_code) {
    let xml = Blockly.Xml.textToDom(xml_code)
    Blockly.Xml.domToWorkspace(xml, this.workspace);
  }

  clear () {
    this.workspace.clear()
  }
}
