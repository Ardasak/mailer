class styles_black_background:
    check_style = """QCheckBox{
        color: white;
    }
    """
    list_style = """QListWidget{
            color: white;
        }"""
    login_style = """QLineEdit{
            height: 20px;
            width: 1000px;
            color: white;
            background: black;
            padding: 5px;
        }
        QPushButton{
            height: 45px;
            width: 60px;
            background: black;
            color: white;
            border: 1px solid black;
            border-radius: 10px;
        }"""
    button_new_page_style = """QPushButton{
            height: 45px;
            background: black;
            border: 1px solid black;
            border-radius: 10px;
        }"""

    add_button_style = """QPushButton{
        width: 60px;
        height: 60px;
        background: black;
        border: 1px solid black;
        border-radius: 5px;
        }"""
    search_field_style = """QLineEdit{
        height: 50px;
        width: 1000px;
        color: white;
        background: black;
        padding: 5px;
        }"""
    subject_and_mail_style = """
    QLineEdit{
        height: 50px;
        width: 1000px;
        color: white;
        background: black;
        padding: 5px;
    }
    QTextEdit{
        color: white;
        padding: 5px;
        }"""
    combobox_style = """QComboBox{
        height: 40px;
        width: 603.25px;
        border: 2px solid white;
        background: black;
        color: white;
        }
        QComboBox QAbstractItemView {
            background-color: black; 
            color: white;
            border-radius: 10px;
        }"""
    menubar_style = """
    QMenuBar{
    background-color: #302F2F;
    color: white;
    }

    QMenuBar::item{
        background: transparent;
    }

    QMenuBar::item:selected{
        background: #99ccff;
        color: black;
        border: 1px solid #3A3939;
    }

    QMenuBar::item:pressed{
        border: 1px solid #3A3939;
        background-color: #99ccff;
        color: black;
        margin-bottom:-1px;
        padding-bottom:1px;
    }
    """
    menu_style = """
    QMenu::item{
        color: white;
    }
    QMenu::item:selected{
        color: black;
        background-color: #99ccff;
    }
    """