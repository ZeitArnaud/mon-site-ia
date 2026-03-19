import { createClient } from '@supabase/supabase-js'

// On force le site à ne pas mettre les résultats en mémoire (pour voir les news direct)
export const revalidate = 0;

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

export default async function Home() {
  // On récupère les articles et on trie par date de création
  const { data: articles, error } = await supabase
    .from('articles')
    .select('*')
    .order('created_at', { ascending: false })

  // C'est ici qu'on débugue : regarde ton TERMINAL (le texte noir) après avoir rafraîchi la page
  console.log("Articles récupérés :", articles);
  if (error) console.error("Erreur détaillée :", error);

  return (
    <main className="min-h-screen bg-gray-50 p-8 font-sans">
      <div className="max-w-4xl mx-auto">
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-extrabold text-blue-600 mb-2 tracking-tight">IA par Métiers</h1>
          <p className="text-gray-600">L'actualité de l'intelligence artificielle pour votre profession.</p>
        </header>

        {/* Si la liste est vide, on affiche un petit message d'attente */}
        {(!articles || articles.length === 0) && (
          <div className="text-center p-10 bg-white rounded-xl border-2 border-dashed border-gray-200">
            <p className="text-gray-400">Aucun article trouvé dans la base de données... pour le moment !</p>
          </div>
        )}

        <div className="grid gap-6">
          {articles?.map((article) => (
            <div key={article.link} className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
              <div className="flex items-center gap-2 mb-3">
                <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-[10px] font-bold uppercase">
                  {article.category}
                </span>
                <span className="text-gray-400 text-[10px]">
                   {new Date(article.created_at).toLocaleDateString('fr-FR')}
                </span>
              </div>
              <h2 className="text-xl font-bold text-gray-800 mb-2 leading-snug">{article.title}</h2>
              <p className="text-gray-600 mb-4 text-sm line-clamp-2">{article.summary}</p>
              <a 
                href={article.link} 
                target="_blank" 
                className="text-blue-600 font-semibold hover:text-blue-800 text-sm inline-flex items-center"
              >
                Lire l'article original 
                <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
              </a>
            </div>
          ))}
        </div>
      </div>
    </main>
  )
}