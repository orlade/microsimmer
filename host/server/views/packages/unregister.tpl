% rebase('base.tpl', title='Unregister')

<h2>Unregister {{name}}</h2>

<form method="POST" action="/packages/{{package}}/unregister">
    <div>Are you sure you want to unregister <b>{{package}}</b>?</div>
    <div><input type="submit" value="Confirm"/></div>
</form>