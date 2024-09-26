def print_parameters(data: Parameters) -> None:
    print("=============== Configuration ===============\n")
    
    print("### General Parameters ###\n")
    print("-> Model Parameters")
    print(f"        Model_ID = {data.model_id}")
    print(f"        Export_Model_to_Binary_File = {data.export_model_to_binary_file}")
    print(f"        Plot_Model = {data.plot_model_bool}")
    print(f"        Model_Smoothing = {data.model_smoothing_bool}")
    print(f"        Smooth_Level = {data.smooth_level}\n")
    
    print("-> Export Model Path")
    print(f"        Binary_Model_Path = {data.binary_model_path}\n")
    
    print("-> VS Velocity Approximation")
    print(f"        VS_Velocity = {data.vs_velocity_approximation}\n")
    
    print("-> Density Value Approximation")
    print(f"        Density_Value = {data.rho_value_approximation}\n")

    print("### Image to Model Area ###\n")
    print("-> Model Bools")
    print(f"        Image_To_Model_ID = {data.image_to_model_id}")
    print(f"        Model_Extra_Routine = {data.model_extra_routine}\n")
    
    print("-> Load Image Model")
    print(f"        Image_File_Path = {data.image_file_path}\n")
    
    print("-> Model Parameters")
    print(f"        VP_Velocity = {data.vp_velocity}")
    print(f"        VS_Velocity = {data.vs_velocity}")
    print(f"        Rho_Value = {data.rho_value}\n")
    
    print("### Complex Image Model ###\n")
    print("-> Model Bools")
    print(f"        Complex_Model_ID = {data.complex_model_bool}")
    print(f"        Inverse_Velocity = {data.inverse_velocity}\n")

    print("-> Model Parameters")
    print(f"        Minimum_VP_Velocity = {data.vpmin}")
    print(f"        Maximum_VP_Velocity = {data.vpmax}")
    print(f"        Minimum_VS_Velocity = {data.vsmin}")
    print(f"        Maximum_VS_Velocity = {data.vsmax}")
    print(f"        Minimum_Density = {data.rhomin}")
    print(f"        Maximum_Density = {data.rhomax}\n")
    
    print("### Parallel Plane Model Area ###\n")
    print("-> Model Bools")
    print(f"        Parallel_Plane_Model_ID = {data.parallel_plane_model_id}\n")
    
    print("-> Model Parameters")
    print(f"        Nx = {data.nx}")
    print(f"        Nz = {data.nz}")
    print(f"        Interfaces = {data.interfaces}")
    print(f"        VP_Velocity = {data.vp_interfaces}")
    print(f"        VS_Velocity = {data.vs_interfaces}")
    print(f"        Rho_Value = {data.rho_interfaces}\n")
    
    print("============================================\n")
