// Confirmar exclusão
function confirmarExclusao(event, id) {
    if (!confirm('Tem certeza que deseja excluir?')) {
        event.preventDefault();
    }
}

// Inicialização quando o documento estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    // Exibir alertas de flash
    const alertas = document.querySelectorAll('.alert');
    alertas.forEach(function(alerta) {
        setTimeout(function() {
            alerta.classList.add('fade');
            setTimeout(function() {
                alerta.remove();
            }, 500);
        }, 3000);
    });
});

