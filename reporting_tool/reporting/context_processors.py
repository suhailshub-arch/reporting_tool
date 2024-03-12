def font_size_processor(request):
    if request.user.is_authenticated:
        return {
            'user_font_size': request.user.userprofile.font_size,
            'user_background_color': request.user.userprofile.background_color,
            'user_font_color': request.user.userprofile.font_color,
            'user_font_type': request.user.userprofile.font_type,
            'user_character_spacing': request.user.userprofile.character_spacing,
            'user_line_height': request.user.userprofile.line_height,
        }
    return {}