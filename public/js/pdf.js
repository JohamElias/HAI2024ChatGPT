const sendPDFRequest= (jsonString)=> {
    const url = "http://localhost:3000/html/pdf";
    const data = jsonString;
    console.log("llegó hasta aquí");
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: data
    })
    .then(response => response.blob())
    .then(blob => {
      // Crear un URL para el blob
      const blobUrl = URL.createObjectURL(blob);
      // Crear un nuevo elemento <a> temporal y simular un click para descargar
      const link = document.createElement('a');
      link.href = blobUrl;
      link.download = "generated_pdf.pdf"; // Puedes personalizar el nombre del archivo
      document.body.appendChild(link); // Añadir el enlace al documento
      link.click(); // Simular click
      document.body.removeChild(link); // Limpiar: quitar el enlace del documento
    })
    .catch(error => console.error('Error al generar el PDF:', error));
  }
  
export default sendPDFRequest;
  