from OpenGL import GL as gl



def get_system_info(should_print=False):
    """
    Get render system informations.

    Args:
        should_print

    Returns:
        str: returns the system infos.
    """
    system_info = f"Your System:"
    system_info += f"\n  > Vendor: {gl.glGetString(gl.GL_VENDOR).decode('utf-8')}"
    system_info += f"\n  > Renderer: {gl.glGetString(gl.GL_RENDER).decode('utf-8')}"
    system_info += f"\n  > OpenGL Version Support: {gl.glGetString(gl.GL_VERSION).decode('utf-8')}"
    system_info += f"\n  > GLSL Version Support: {gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION).decode('utf-8')}"
    return system_info



def compile_glsl_shader_code(shader_code, shader_type, version="3.3.0"):
    """
    Create and Shader Object and
    compile GLSL Shader Code and return the shader object.

    Args:
        shader_code (str): Shader Code in C.
        shader_type (str): The type of your shader.
        version (str): OpenGL/GLSL version.

    Raises:
        RuntimeException: If compilation fails.

    Returns:
        OpenGL.GL.ShaderReference (FIXME): The shader reference/object.
    """
    # add OpenGL/GLSL version
    shader_code = f'#version {"".join(version.split("."))}\n' + shader_code

    # create shader object
    shader_ref = gl.glCreateShader(shader_type)

    # store shader code in shader obj
    gl.glShaderSource(shader_ref, shader_code)

    # compile shader code
    gl.glCompileShader(shader_ref)

    # check compiling process
    compiling_succeded = gl.glGetShaderiv(shader_ref, gl.GL_COMPILE_STATUS)

    if not compiling_succeded:
        error_msg = gl.glGetShaderInfoLog(
            gl.glDeleteShader(shader_ref)
        )
        raise RuntimeError("\n" + error_msg.decode("utf-8"))
    
    return shader_ref



def create_glsl_program(vertex_shader_code, fragment_shader_code, version="3.3.0"):
    """
    Create a the shader programm and call the shader compilation.

    Args:
        vertex_shader_code (str): Shader Code in C for Vertexes.
        fragment_shader_code (str): Shader Code in C for Fragmants.
        version (str): OpenGL/GLSL version.

    Returns:
        OpenGL.GL.Program (FIXME): The shader program reference/object.
    """
    # compile shader code
    vertex_shader_ref = compile_glsl_shader_code(shader_code=vertex_shader_code, 
                                                 shader_type=gl.GL_VERTEX_SHADER, 
                                                 version=version)
    
    fragmant_shader_ref = compile_glsl_shader_code(shader_code=fragment_shader_code, 
                                                   shader_type=gl.GL_FRAGMENT_SHADER, 
                                                   version=version)
    
    # create shader program
    programm_ref = gl.glCreateProgram()

    # add shader code to the program
    gl.glAttachShader(programm_ref, vertex_shader_ref)
    gl.glAttachShader(programm_ref, fragmant_shader_ref)

    # link vertex and fragmant shaders
    gl.glLinkProgram(programm_ref)

    # check linking process
    link_succeded = gl.glGetProgramiv(programm_ref, gl.GL_LINK_STATUS)
    if not link_succeded:
        error_msg = gl.glGetProgramInfoLog(programm_ref)
        gl.glDeleteProgram(programm_ref)
        raise RuntimeError("\n"+error_msg.decode("utf-8"))
    
    return programm_ref


