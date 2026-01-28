export default function Section({ data }) {
  if (!data || !data.items) return null

  return (
    <section className="py-16 px-4 bg-gray-50">
      <div className="max-w-7xl mx-auto">
        {/* Intro Section */}
        {data.section_type === 'intro' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Content Column */}
            <div className="space-y-6">
              {data.items[0]?.title && (
                <h2 className="text-4xl lg:text-5xl font-bold text-gray-800 leading-tight font-sans">{data.items[0].title}</h2>
              )}
              {data.items[0]?.subtitle && (
                <h3 className="text-xl lg:text-2xl text-gray-600 font-sans">{data.items[0].subtitle}</h3>
              )}
              {data.items[0]?.description && (
                <p className="text-lg text-gray-700 leading-relaxed font-sans">{data.items[0].description}</p>
              )}
            </div>
            
            {/* Image Column */}
            {data.items[0]?.image && (
              <div className="order-first lg:order-last">
                <img 
                  src={data.items[0].image} 
                  alt={data.items[0].title} 
                  className="w-full h-auto rounded-lg object-cover"
                />
              </div>
            )}
          </div>
        )} 

        {/* Services Section */}
        {data.section_type === 'services' && (
          <div>
            <h2 className="text-4xl font-bold text-center mb-12">Our Services</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {data.items.map((item, idx) => (
                <div key={idx} className="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition duration-300">
                  {item.image && (
                    <img src={item.image} alt={item.title} className="w-full h-48 object-cover rounded-lg mb-4" />
                  )}
                  {item.icon && <div className="text-5xl mb-4">{item.icon}</div>}
                  {item.title && <h3 className="text-2xl font-bold mb-3">{item.title}</h3>}
                  {item.description && <p className="text-gray-600 mb-4">{item.description}</p>}
                  {item.button_text && (
                    <a
                      href={item.button_link || '#'}
                      className="text-blue-600 hover:text-blue-700 font-semibold"
                    >
                      {item.button_text} →
                    </a>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  )
}
