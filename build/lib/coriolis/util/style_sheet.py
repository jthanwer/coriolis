def get_style_sheet():
    ss = """
    
    /* QWidget ------------------------------------------------------------ */
    
    QWidget{
        background-color: #eaf8fb;
        font:large "Comic Sans MS";
    }
    
 
    /* QMainWindow ------------------------------------------------------------ */

    QMainWindow::separator {
        background-color: #eaf8fb;
    }
    
    
    /* QMenuBar ------------------------------------------------------------ */

    QMenuBar {
        background-color: #32414b;
        padding: 2px;
        border: 1px solid #19232d;
        color: #F0F0F0;
        font-size: 12pt;
    }
    
    QMenuBar:focus {
        border: 1px solid #148cd2;
    }
     
    QMenuBar::item {
        background: transparent;
        padding: 4px;
    }

    QMenuBar::item:selected {
        padding: 4px;
        background: transparent;
        border: 0px solid #148cd2;
    }

    QMenuBar::item:pressed {
        padding: 4px;
        border: 0px solid #32414B;
        background-color: #148CD2;
        color: white;
        margin-bottom: 0px;
        padding-bottom: 0px;
    }
    
    QMenu {
        border: 0px solid #32414B;
        color: black;
        background-color: #eaf8fb;
        margin: 0px;
    }
    

    QMenu::separator {
        height: 2px;
        background-color: #505F69;
        color: #F0F0F0;
        padding-left: 4px;
        margin-left: 2px;
        margin-right: 2px;
}


    QMenu::item {
        padding: 4px 24px 4px 24px;
        border: 1px transparent #eaf8fb;
    }

    QMenu::item:selected {
        background-color: #148cd2;
        color: white;
    }
    
    QMenu::indicator {
        width: 12px;
        height: 12px;
        padding-left:6px;
    }
    
    /* ------------------------------------------------------------------------------ */
    /* GROUP BOXES ------------------------------------------------------------------ */
    /* ------------------------------------------------------------------------------ */
    
    
    QGroupBox {
        color: #32414b;
        font-size: 10pt;
        font-weight: bold;     
    }
    
    
    /* ---------------------------------------------------------------------------- */
    /* CHECK BOXES ---------------------------------------------------------------- */
    /* ---------------------------------------------------------------------------- */
    
    QCheckBox{
        background-color: #eaf8fb;
        color: black;
    }
    
    QCheckBox::indicator:hover {
       background-color: white;
       color: black;
       border: 2px solid black;
    }
    
    QCheckBox::indicator:checked:pressed {
       background-color: black;
    
    }
    
    
    /* ------------------------------------------------------------------------ */
    /* TREES ------------------------------------------------------------------ */
    /* ------------------------------------------------------------------------ */
    
    
    QTreeView {
    background-color: white;
    }
    
    QTreeView::item:has-children {
    background-color: #e6e6ff;
    }
    
    /* ------------------------------------------------------------------------- */
    /* TABLES ------------------------------------------------------------------ */
    /* ------------------------------------------------------------------------- */
    
    
    QTableWidget {
    background-color: white;
    }
    
    
    /* ------------------------------------------------------------------------ */
    /* BUTTONS ---------------------------------------------------------------- */
    /* ------------------------------------------------------------------------ */
    
    /* QPushButton ------------------------------------------------------------ */
    
    
    QPushButton {
        background-color: rgb(240, 240, 255) ;
        color: rgb(50, 0, 0);
        border: 2px solid rgb(180, 180, 255);
        padding: 7px 7px 7px 7px;
        border-radius: 10px;
        margin: 0px 0px 0px 0px;
    }

    QPushButton:checked {
        background-color: rgb(180, 180, 255) ;
    }
    
    QPushButton:pressed {
        background-color: rgb(180, 180, 255) ;
    }
    
    /* -----------------------------------------------------------------------------*/
    /* COMBO BOXES ---------------------------------------------------------------- */
    /* ---------------------------------------------------------------------------- */
    
    
    QComboBox {
        border: 1px solid #32414B; 
        border-radius: 4px; 
        background-color: rgb(240, 240, 255);
        selection-background-color: rgb(180, 180, 255);
        color: black;
        padding-top: 2px;
        padding-bottom: 2px;
        padding-left: 4px; 
        padding-right: 4px;
    }
    
    QComboBox:disabled {
        background-color: rgb(240, 240, 255);
        color: black;
    }
    

    QComboBox:on {
        background-color: rgb(240, 240, 255);
        color: black;
    }
    
    
    """

    return ss
