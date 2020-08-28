args = {

    1:{
        'module':'initialize_env',
        'args':['azure_user','azure_pass','git_token'],
        'desc':'initialize the setup environment'
    },
    
    2:{
        'module':'configuration_manager',
        'args':['key_val','command','category'],
        'desc':'add, update, and remove configurations from the configuration dictionary'
    },

    3:{
        'module':'new_project_initializer',
        'args':'project_name',
        'desc':'initializes new project'
    }
    
}