"""
Script pour configurer le theme Django Admin Interface
avec les couleurs Pinnacle Supply Chain (Bleu/Vert)
"""
import os
import sys
import django

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from admin_interface.models import Theme


def configure_theme():
    """Configure le thème admin avec les couleurs Pinnacle"""

    # Récupérer ou créer le thème
    theme, created = Theme.objects.get_or_create(pk=1)

    if created:
        print("✅ Nouveau thème créé")
    else:
        print("🔄 Thème existant trouvé - mise à jour")

    # Configuration générale
    theme.name = "Pinnacle Supply Chain"
    theme.title = "Pinnacle Supply Chain"
    theme.title_visible = True

    # Couleurs principales (Bleu Pinnacle)
    theme.title_color = "#3B82F6"  # Bleu
    theme.css_header_background_color = "#3B82F6"  # Bleu header
    theme.css_header_text_color = "#FFFFFF"  # Texte blanc
    theme.css_header_link_color = "#FFFFFF"  # Liens blancs
    theme.css_header_link_hover_color = "#10B981"  # Vert au hover

    # Menu latéral
    theme.css_module_background_color = "#F9FAFB"  # Gris très clair
    theme.css_module_text_color = "#1F2937"  # Gris foncé
    theme.css_module_link_color = "#3B82F6"  # Bleu
    theme.css_module_link_hover_color = "#10B981"  # Vert au hover
    theme.css_module_rounded_corners = True

    # Boutons actions
    theme.css_save_button_background_color = "#10B981"  # Vert
    theme.css_save_button_background_hover_color = "#059669"  # Vert foncé
    theme.css_save_button_text_color = "#FFFFFF"

    theme.css_delete_button_background_color = "#EF4444"  # Rouge
    theme.css_delete_button_background_hover_color = "#DC2626"  # Rouge foncé
    theme.css_delete_button_text_color = "#FFFFFF"

    # Generic relations
    theme.related_modal_active = True
    theme.related_modal_background_color = "#F9FAFB"
    theme.related_modal_rounded_corners = True

    # Liste
    theme.list_filter_dropdown = True
    theme.list_filter_sticky = True

    # Footer
    theme.css_generic_link_color = "#3B82F6"  # Bleu
    theme.css_generic_link_hover_color = "#10B981"  # Vert

    # Sauvegarder
    theme.save()

    print("\n✅ THÈME CONFIGURÉ AVEC SUCCÈS!")
    print("\n📋 Configuration appliquée:")
    print(f"   - Titre: {theme.title}")
    print(f"   - Couleur principale: {theme.css_header_background_color} (Bleu)")
    print(f"   - Couleur secondaire: {theme.css_save_button_background_color} (Vert)")
    print(f"   - Boutons sauvegarde: {theme.css_save_button_background_color}")
    print(f"   - Liens: {theme.css_generic_link_color}")
    print("\n🌐 Visitez: http://localhost:8000/admin/")
    print("   Le nouveau thème sera appliqué immédiatement!")


if __name__ == '__main__':
    configure_theme()
