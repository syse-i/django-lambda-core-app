from allauth.account.adapter import DefaultAccountAdapter


class AccountAdapter(DefaultAccountAdapter):

    def render_mail(self, template_prefix, email, context):
        return super().render_mail(template_prefix, email, context)
