package specs

import pages.HomePage
import pages.NewCreditTransferPage
import pages.CreditTransactionsPage
import pages.ConfirmSubmitModal
import pages.NotificationsPage
import pages.CreditTransactionsViewPage
import pages.CreditTransactionsConfirmAcceptModal
import pages.CreditTransactionsConfirmRecommendModal
import pages.CreditTransactionsConfirmApproveModal
import pages.ToastModal

import spock.lang.Title
import spock.lang.Narrative
import spock.lang.Stepwise
import spock.lang.Shared

@Stepwise
@Title('Credit Transfer Test')
@Narrative('''As a fuel supplier, I want to transfer credits to another fuel supplier.''')
class CreditTransferSpec extends LoggedInSpec {

  @Shared
  Integer sendingFuelSupplier_initialCreditBalance

  @Shared
  Integer receivingFuelSupplier_initialCreditBalance

  void 'Log in as the sending fuel supplier and initiate a new credit transfer'() {
    given: 'I am logged in as the sending fuel supplier'
      logInAsSendingFuelSupplier()
      to CreditTransactionsPage
      sendingFuelSupplier_initialCreditBalance = getCreditBalance()
      sleep(5000)
    and: 'I populate all required fields for a new credit transfer'
      to NewCreditTransferPage
      setTransactionType('Sell')
      setNumberOfCredits(98)
      setRespondent(getReceivingFuelSupplier().org)
      setPricePerCredit(2)
      checkTerms()
      addComment('Log in as the sending fuel supplier and initiate a new credit transfer')
    when: 'I sign 1 of 2 and submit the transfer'
      signCreditTransfer()
      page(ConfirmSubmitModal)
      sleep(5000)
      clickYesButton()
    then: 'The credit transfer is initiated and I am returned to the Credit Transactions page'
      at CreditTransactionsPage
  //  and: 'I am shown a success toast popup'
  //    at new ToastModal('Success!', 'Credit Transfer Proposal sent.')
      and: 'My credit balance has not changed'
        page(CreditTransactionsPage)
        getCreditBalance() == sendingFuelSupplier_initialCreditBalance
        sleep(10000)
  }

  void 'Log in as the receiving fuel supplier and accept the credit transfer'() {
    given: 'I am logged in as the receiving fuel supplier'
      logInAsReceivingFuelSupplier()
      to CreditTransactionsPage
      receivingFuelSupplier_initialCreditBalance = getCreditBalance()
    and: 'I populate all required fields to accept the proposed credit transfer'
      to NotificationsPage
      getCreditTransferLinkByText('Credit Transfer Proposal Proposed').click()
      page(new CreditTransactionsViewPage('Credit Transfer'))
      checkTerms()
      addComment('Log in as the receiving fuel supplier and accept the credit transfer')
    when: 'I sign 2 of 2 and submit the transfer'
      signCreditTransfer()
      page(CreditTransactionsConfirmAcceptModal)
      acceptCreditTransaction()
    then: 'The credit transfer is accepted and I am returned to the Credit Transactions page'
      at CreditTransactionsPage
   // and: 'I am shown a success toast popup'
     // at new ToastModal('Success!', 'Credit Transfer Proposal accepted.')
    and: 'My credit balance has not changed'
      page(CreditTransactionsPage)
      getCreditBalance() == receivingFuelSupplier_initialCreditBalance
      sleep(10000)
  }

  void 'Log in as an analyst and recommend the credit transfer'() {
    given: 'I am logged in as an Analyst'
      logInAsAnalyst()
    and: 'I populate all required fields to recommend the accepted credit transfer'
      to NotificationsPage
      getCreditTransferLinkByText('Credit Transfer Proposal Signed').click()
      page(new CreditTransactionsViewPage('Credit Transfer'))
      addComment('Log in as an analyst and recommend the credit transfer')
      addInternalComment('Log in as an analyst and recommend the credit transfer')
    when: 'I recommend and confirm the transfer'
      recommendCreditTransfer()
      page(CreditTransactionsConfirmRecommendModal)
      recommendCreditTransaction()
    then: 'The credit transfer is recommended and I am returned to the Credit Transactions page'
      at CreditTransactionsPage
      sleep(10000)
   // and: 'I am shown a success toast popup'
   //   at new ToastModal('Success!', 'Credit Transfer Proposal recommended.')
  }

  void 'Log in as a Director and approve the credit transfer'() {
    given: 'I am logged in as a Director'
      logInAsDirector()
    and: 'I populate all required fields to approve the recommended credit transfer'
      to NotificationsPage
      getCreditTransferLinkByText('Credit Transfer Proposal Recommended For Approval').click()
      page(new CreditTransactionsViewPage('Credit Transfer'))
      addComment('Log in as a Director and approve the credit transfer')
      addInternalComment('Log in as a Director and approve the credit transfer')
    when: 'I approve and confirm the transfer'
      approveCreditTransfer()
      page(CreditTransactionsConfirmApproveModal)
      approveCreditTransaction()
    then: 'The credit transfer is approved and I am returned to the Credit Transactions page'
      at CreditTransactionsPage
      sleep(10000)
   // and: 'I am shown a success toast popup'
    //  at new ToastModal('Success!', 'Credit Transfer Proposal approved.')
  }

  void 'Log in as the sending fuel supplier and verify my credit balance has decreased'() {
    given: 'I am logged in as the sending fuel supplier'
      logInAsSendingFuelSupplier()
      to CreditTransactionsPage
    when: 'I have previously successfully transferred credits to another fuel supplier'
    then: 'My credit balance is decreased by the amount transferred'
      getCreditBalance() == sendingFuelSupplier_initialCreditBalance - 98
      sleep(10000)
  }

  void 'Log in as the receiving fuel supplier and verify my credit balance has increased'() {
    given: 'I am logged in as the receiving fuel supplier'
      logInAsReceivingFuelSupplier()
      to CreditTransactionsPage
    when: 'I have previously successfully been transferred credits from another fuel supplier'
    then: 'My credit balance is increased by the amount transferred'
      getCreditBalance() == receivingFuelSupplier_initialCreditBalance + 98
      sleep(10000)
  }

}
