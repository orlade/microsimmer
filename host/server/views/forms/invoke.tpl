<form method="POST" action="/packages/{{package}}/{{service}}/invoke" enctype="multipart/form-data">
    <p>Invoke <b></b>{{package}}/{{service}}</p>

    <table>
        % for param in params:
        <tr>
            <td>{{param}}</td>
            <!-- File upload will override text input if provided. -->
            <td><input name="{{param}}"/>, or <input type="file" name="__file__{{param}}"/></td>
        </tr>
        % end
    </table>

    <input type="submit" value="Run"/>
</form>