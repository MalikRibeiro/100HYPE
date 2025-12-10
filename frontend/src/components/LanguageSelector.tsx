import { useTranslation } from 'react-i18next';
import { Button } from "@/components/ui/button";

export function LanguageSelector() {
    const { i18n } = useTranslation();

    const toggleLanguage = () => {
        const newLang = i18n.language.startsWith('pt') ? 'en' : 'pt';
        i18n.changeLanguage(newLang);
    };

    return (
        <Button
            variant="ghost"
            size="sm"
            onClick={toggleLanguage}
            className="w-12 px-0 font-bold"
        >
            {i18n.language.startsWith('pt') ? 'BR' : 'EN'}
        </Button>
    );
}
