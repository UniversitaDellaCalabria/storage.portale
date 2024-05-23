const forcePasteAsPlainText = () => {
    Object.values(editors).forEach(editor => {
        const editingView = editor.editing.view;
    
        editingView.document.on( 'clipboardInput', ( evt, data ) => {
            if ( editor.isReadOnly ) {
                return;
            }
            let content = data.dataTransfer.getData('text/plain');
            data.content = editor.data.htmlProcessor.toView( content );
            editingView.scrollToTheSelection();
        }, { priority: 'high' } ); 
    });
};

$(() => {
    forcePasteAsPlainText();
});