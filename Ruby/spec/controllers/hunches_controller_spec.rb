require 'spec_helper'

# This spec was generated by rspec-rails when you ran the scaffold generator.
# It demonstrates how one might use RSpec to specify the controller code that
# was generated by the Rails when you ran the scaffold generator.

describe HunchesController do

  def mock_hunch(stubs={})
    @mock_hunch ||= mock_model(Hunch, stubs).as_null_object
  end

  describe "GET index" do
    it "assigns all hunches as @hunches" do
      Hunch.stub(:all) { [mock_hunch] }
      get :index
      assigns(:hunches).should eq([mock_hunch])
    end
  end

  describe "GET show" do
    it "assigns the requested hunch as @hunch" do
      Hunch.stub(:find).with("37") { mock_hunch }
      get :show, :id => "37"
      assigns(:hunch).should be(mock_hunch)
    end
  end

  describe "GET new" do
    it "assigns a new hunch as @hunch" do
      Hunch.stub(:new) { mock_hunch }
      get :new
      assigns(:hunch).should be(mock_hunch)
    end
  end

  describe "GET edit" do
    it "assigns the requested hunch as @hunch" do
      Hunch.stub(:find).with("37") { mock_hunch }
      get :edit, :id => "37"
      assigns(:hunch).should be(mock_hunch)
    end
  end

  describe "POST create" do
    describe "with valid params" do
      it "assigns a newly created hunch as @hunch" do
        Hunch.stub(:new).with({'these' => 'params'}) { mock_hunch(:save => true) }
        post :create, :hunch => {'these' => 'params'}
        assigns(:hunch).should be(mock_hunch)
      end

      it "redirects to the created hunch" do
        Hunch.stub(:new) { mock_hunch(:save => true) }
        post :create, :hunch => {}
        response.should redirect_to(hunch_url(mock_hunch))
      end
    end

    describe "with invalid params" do
      it "assigns a newly created but unsaved hunch as @hunch" do
        Hunch.stub(:new).with({'these' => 'params'}) { mock_hunch(:save => false) }
        post :create, :hunch => {'these' => 'params'}
        assigns(:hunch).should be(mock_hunch)
      end

      it "re-renders the 'new' template" do
        Hunch.stub(:new) { mock_hunch(:save => false) }
        post :create, :hunch => {}
        response.should render_template("new")
      end
    end
  end

  describe "PUT update" do
    describe "with valid params" do
      it "updates the requested hunch" do
        Hunch.stub(:find).with("37") { mock_hunch }
        mock_hunch.should_receive(:update_attributes).with({'these' => 'params'})
        put :update, :id => "37", :hunch => {'these' => 'params'}
      end

      it "assigns the requested hunch as @hunch" do
        Hunch.stub(:find) { mock_hunch(:update_attributes => true) }
        put :update, :id => "1"
        assigns(:hunch).should be(mock_hunch)
      end

      it "redirects to the hunch" do
        Hunch.stub(:find) { mock_hunch(:update_attributes => true) }
        put :update, :id => "1"
        response.should redirect_to(hunch_url(mock_hunch))
      end
    end

    describe "with invalid params" do
      it "assigns the hunch as @hunch" do
        Hunch.stub(:find) { mock_hunch(:update_attributes => false) }
        put :update, :id => "1"
        assigns(:hunch).should be(mock_hunch)
      end

      it "re-renders the 'edit' template" do
        Hunch.stub(:find) { mock_hunch(:update_attributes => false) }
        put :update, :id => "1"
        response.should render_template("edit")
      end
    end
  end

  describe "DELETE destroy" do
    it "destroys the requested hunch" do
      Hunch.stub(:find).with("37") { mock_hunch }
      mock_hunch.should_receive(:destroy)
      delete :destroy, :id => "37"
    end

    it "redirects to the hunches list" do
      Hunch.stub(:find) { mock_hunch }
      delete :destroy, :id => "1"
      response.should redirect_to(hunches_url)
    end
  end

end