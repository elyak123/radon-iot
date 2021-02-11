from radon.users.auth import ClienteAutenticationMixin


class CrmTemplateSelector(ClienteAutenticationMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["template"] = 'crm/base.html'
        return context
